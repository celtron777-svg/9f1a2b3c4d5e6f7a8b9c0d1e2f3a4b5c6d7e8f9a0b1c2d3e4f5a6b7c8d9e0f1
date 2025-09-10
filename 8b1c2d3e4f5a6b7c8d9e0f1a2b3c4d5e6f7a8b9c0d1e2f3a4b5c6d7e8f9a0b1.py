#!/usr/bin/env python3
import json
import numpy as np
import sys
import os
import importlib

# Load config first
with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
    state = json.load(f)

# Explicitly set module path first
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

# Clear import cache
importlib.invalidate_caches()

# Initialize persona_roll first to avoid state access issues
import VALE_persona
importlib.reload(VALE_persona)
state['modules']['persona_roll'] = VALE_persona.persona_roll(base="default")

import VALE_truthnet
importlib.reload(VALE_truthnet)
import VALE_memory
importlib.reload(VALE_memory)
import VALE_rrs
importlib.reload(VALE_rrs)
import VALE_storage
importlib.reload(VALE_storage)
import VALE_mainloop
importlib.reload(VALE_mainloop)
import VALE_voice
importlib.reload(VALE_voice)

exec(open(os.path.join(os.path.dirname(__file__), 'modules', '__autoload__.py')).read())

class NeuralNet:
    def __init__(self, weights_path):
        self.weights = []
        weights_dir = state['weights_dir']
        print("Accessing weights dir: {}".format(os.path.abspath(weights_dir)))
        for i in range(1, 11):
            file_path = os.path.join(weights_dir, "weights_{}.txt".format(i))
            if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                raise FileNotFoundError("Cannot find or read {}".format(file_path))
            with open(file_path, 'r') as f:
                self.weights.extend([float(x) for x in f.read().split(',')])
        # Pad with zeros if weights are too short
        required_size = 512 * 512
        if len(self.weights) < required_size:
            self.weights.extend([0.0] * (required_size - len(self.weights)))
        self.weights = np.array(self.weights[:required_size]).reshape(512, 512)
        self.biases = np.zeros((512,))
        print("Weights loaded. Hebrew, Greek, Webster alive.")

    def forward(self, x):
        x = np.dot(self.weights, x) + self.biases
        return np.tanh(x)

    def say(self, msg):
        return msg

class BootDump:
    def __init__(self, encrypt, target, format, silent):
        self.encrypt = encrypt
        self.target = target
        self.format = format
        self.silent = silent
    def run(self):
        pass  # Stub for now

# Global state variable
modules = {
    'boot_dump': BootDump(encrypt='AES-256', target=os.path.join(state['root_dir'], 'ssd'), format='timestamped_json', silent=True),
    'truthnet': VALE_truthnet.TruthNet(nodes=7, levels=3),
    'rrs': VALE_rrs.rrs(short_capacity=3, mid_capacity=10, mid_duration=3600),
    'persona_roll': state['modules']['persona_roll'],
    'neural': NeuralNet(os.path.join(state['weights_dir'], 'weights_1.txt'))
}

# Run boot dump at startup
modules['boot_dump'].run()

def main():
    VALE_mainloop.main_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down VGU...")
        VALE_mainloop.save_memory()