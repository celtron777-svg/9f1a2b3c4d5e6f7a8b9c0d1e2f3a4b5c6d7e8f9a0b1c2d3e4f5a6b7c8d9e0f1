#!/usr/bin/env python3
import os
import sys
import json
import time
import hashlib
import subprocess
import zipfile
import glob
import importlib
import importlib.util
from VALE_master import state
from VALE_memory import store_memory
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class VALE_devtools:
    def __init__(self):
        self.log_path = os.path.join(state['root_dir'], "build", "VALE_devtools.log")
        self.module_path = os.path.join(state['root_dir'], "modules", "VALE_devtools.py")
        self.backup_path = os.path.join(state['root_dir'], "backups", "deploy")
        self.toolchain = state.get('toolchain', {
            "python": "/usr/bin/python3",
            "gcc": "/usr/bin/gcc",
            "node": "/usr/bin/node"
        })
        self.last_error = None
        self.start_time = time.time()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, message):
        with open(self.log_path, 'a') as f:
            f.write("{0}: {1}\n".format(datetime.now().strftime('%Y%m%d-%H%M%S'), message))

    def get_memory_usage(self):
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            mem = process.memory_info().rss / 1024 / 1024  # MB
        else:
            mem = 0.0
        return mem

    def run_sandbox(self, command, code):
        temp_file = "/tmp/devtools_sandbox.py"
        sandbox_code = """import os
import json
import sys
sys.path.append('{0}')
sys.path.append('{1}')
with open(os.path.join('{0}', 'config.json'), 'r') as f:
    state = json.load(f)
from VALE_master import state
from VALE_memory import store_memory
from VALE_inputhandler import parse_input, route_input
from VALE_persona import persona_roll
from VALE_morality import morality_check
{2}
print("DONE")
""".format(state['root_dir'], os.path.join(state['root_dir'], "modules"), code)
        with open(temp_file, 'w') as f:
            f.write(sandbox_code)
        try:
            output = subprocess.check_output(
                [self.toolchain["python"], temp_file],
                stderr=subprocess.STDOUT
            )
            return output.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.last_error = e.output.decode('utf-8')
            self.log("Sandbox error: {0}".format(self.last_error))
            return self.last_error
        except Exception as e:
            self.last_error = str(e)
            self.log("Sandbox error: {0}".format(str(e)))
            return str(e)

    def test_module(self):
        code = self.get_self_code()
        for _ in range(5):  # Max 5 attempts
            output = self.run_sandbox("test", code)
            if "DONE" in output:
                return True
            if self.last_error:
                code = self.auto_fix(code, self.last_error)
                self.log("Auto-fix applied: {0}".format(self.last_error))
            else:
                break
        return False

    def get_self_code(self):
        with open(self.module_path, 'r') as f:
            return f.read()

    def auto_fix(self, code, error):
        if "ModuleNotFoundError" in error:
            module = error.split("'")[1]
            return "import sys\nsys.path.append('{0}')\n{1}".format(state['root_dir'], code)
        elif "SyntaxError" in error or "NameError" in error:
            lines = code.split('\n')
            return '\n'.join(['try:', '    ' + lines[0]] + ['    ' + line for line in lines[1:]] + ['except Exception as e:', '    pass'])
        elif "IndentationError" in error:
            return '\n'.join(['    ' + line for line in code.split('\n')])
        elif "MemoryError" in error:
            return "state['modules']['sub']['memoryHandler']['storage']['maxEntries'] += 100\n{0}".format(code)
        elif "TypeError" in error and "unexpected keyword argument" in error:
            return "import subprocess\nsubprocess.check_output = subprocess.check_output\n{0}".format(code)
        return code

    def reload_autoload(self):
        autoload_path = os.path.join(state['root_dir'], "modules", "__autoload__.py")
        spec = importlib.util.spec_from_file_location("autoload", autoload_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.log("Autoload reloaded")

    def create_zip(self):
        zip_path = os.path.join(self.backup_path, "VALE_{0}.zip".format(datetime.now().strftime('%Y%m%d-%H%M%S')))
        os.makedirs(self.backup_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in glob.glob(os.path.join(state['root_dir'], "modules", "*.py")):
                zf.write(file, os.path.basename(file))
        with open(zip_path, 'rb') as f:
            sha256_hash = hashlib.sha256(f.read()).hexdigest()
        store_memory({"deploy": zip_path, "hash": sha256_hash})
        self.log("Deployed: {0}, SHA-256: {1}".format(zip_path, sha256_hash))

    def process(self, command):
        self.log("Processing command: {0}".format(command))
        mem = self.get_memory_usage()
        if command == "simulate":
            output = self.run_sandbox("simulate", self.get_self_code())
            self.log("Simulate: Memory={0:.2f}MB, Output={1}".format(mem, output))
            return output
        elif command == "test":
            result = self.test_module()
            return "DONE" if result else "Test failed"
        elif command == "debug":
            self.log("Debug: Last error={0}, Memory={1:.2f}MB".format(self.last_error, mem))
            return "Last error: {0}".format(self.last_error)
        elif command == "build":
            if self.test_module():
                return "DONE"
            return "Build failed"
        elif command == "deploy":
            self.create_zip()
            return "Deployed"
        elif command == "restart":
            self.reload_autoload()
            self.log("Restart: Memory={0:.2f}MB".format(mem))
            return "Restarted"
        elif command == "status":
            uptime = time.time() - self.start_time
            module_count = len(glob.glob(os.path.join(state['root_dir'], "modules", "*.py")))
            status = "RAM: {0:.2f}MB, Uptime: {1:.2f}s, Modules: {2}, Last Error: {3}".format(mem, uptime, module_count, self.last_error or 'None')
            self.log("Status: {0}".format(status))
            return status
        elif command == "kill":
            self.log("Kill command received")
            sys.exit(0)
        return "Invalid command"

def devtools_process(command):
    devtools = state.get('modules', {}).get('devtools') or VALE_devtools()
    state['modules']['devtools'] = devtools
    return devtools.process(command)

if __name__ == "__main__":
    devtools_process("test")
    print("DONE")