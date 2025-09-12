import sys
from VALE_mainloop import VALE_mainloop
from VALE_autoload import load_modules

class VALEMaster:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.modules = load_modules()

    def initialize(self):
        """Initialize VALE system with all modules."""
        print("Initializing VALE Master...")
        for module_name, module in self.modules.items():
            print("Loaded module: " + str(module_name))
        self.main_loop = VALEMainLoop(self.config_path)

    def run(self):
        """Run the VALE system."""
        try:
            self.initialize()
            self.main_loop.start()
        except Exception as e:
            print("Critical error in VALE Master: " + str(e))
            self.shutdown()

    def shutdown(self):
        """Shutdown the VALE system."""
        print("VALE Master shutting down...")
        self.main_loop.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    master = VALEMaster("/home/celtron/vgu/VALE_config.json")
    master.run()
