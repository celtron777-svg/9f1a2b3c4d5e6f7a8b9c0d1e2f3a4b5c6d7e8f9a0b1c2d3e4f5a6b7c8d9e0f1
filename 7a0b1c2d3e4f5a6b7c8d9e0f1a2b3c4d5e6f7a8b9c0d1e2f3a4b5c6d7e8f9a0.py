import os
import time
import json
from VALE_master import state
from VALE_memory import load_memory, save_memory, store_memory
from VALE_inputhandler import parse_input, route_input
from VALE_persona import persona_roll

# Backup Management
def create_backup():
    """Create a database backup"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = "{}/vgu-backup-{}".format(state['modules']['sub']['backupManager']['backup']['path'], timestamp)
    try:
        os.makedirs(backup_path, exist_ok=True)
        with open("{}/state.json".format(backup_path), "w") as f:
            json.dump(state, f, indent=2)
        store_memory({'backup': backup_path, 'timestamp': timestamp})
        cleanup_backups()
        return "Backup created"
    except Exception as e:
        return "Backup failed: {}".format(str(e))

def restore_backup():
    """Restore from the latest backup"""
    backups = [b['backup'] for b in state['memory'] if 'backup' in b]
    if not backups:
        return "No backups found"
    latest = max(backups, key=lambda x: x.split('-')[-1])
    try:
        with open("{}/state.json".format(latest), "r") as f:
            state.update(json.load(f))
        return "Database restored"
    except Exception as e:
        return "Restore failed: {}".format(str(e))

def cleanup_backups():
    """Remove old backups"""
    backups = [b['backup'] for b in state['memory'] if 'backup' in b]
    if len(backups) > state['modules']['sub']['backupManager']['backup']['maxBackups']:
        oldest = min(backups, key=lambda x: x.split('-')[-1])
        os.remove("{}/state.json".format(oldest))
        os.rmdir(oldest)
        state['memory'] = [b for b in state['memory'] if b.get('backup') != oldest]

# Main Loop
def main_loop():
    """Main interaction loop for VGU"""
    load_memory()
    print("VGU online. {} modules fused. Ready.".format(len(state['mcf']['dependencies'])))
    while True:
        try:
            inp = input("Enter command: ")  # Temporary input
            if inp.lower() == 'quit':
                save_memory()
                break
            if inp.lower() == 'backup':
                print(create_backup())
                continue
            if inp.lower() == 'restore':
                print(restore_backup())
                continue
            parsed = parse_input(inp)
            if parsed.get('error'):
                print(parsed['error'])
                continue
            response = route_input(parsed)
            print(response)
        except Exception as e:
            print("Error: {}".format(str(e)))

# Launcher
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Shutting down VGU...")
        save_memory()