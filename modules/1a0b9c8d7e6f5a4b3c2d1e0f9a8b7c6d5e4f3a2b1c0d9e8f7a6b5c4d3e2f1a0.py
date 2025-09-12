from importlib import import_module
from typing import Dict

def load_modules() -> Dict:
    """Dynamically load all VALE modules."""
    modules = {}
    module_names = [
        "VALE_inputhandler",
        "VALE_memory",
        "VALE_memory_ring",
        "VALE_morality",
        "VALE_persona",
        "VALE_rrs",
        "VALE_security",
        "VALE_storage",
        "VALE_truthnet_core",
        "VALE_truthnet_trace",
        "VALE_voice"
    ]
    for name in module_names:
        try:
            module = import_module("modules." + name)
            modules[name] = getattr(module, name)
        except ImportError as e:
            print("Failed to load module " + name + ": " + str(e))
    return modules
