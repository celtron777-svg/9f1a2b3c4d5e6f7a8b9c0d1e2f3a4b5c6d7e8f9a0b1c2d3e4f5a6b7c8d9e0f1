import os
import time
import json
from VALE_master import state
from VALE_memory import store_memory
from VALE_mainloop import create_backup, cleanup_backups

# Storage Management
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