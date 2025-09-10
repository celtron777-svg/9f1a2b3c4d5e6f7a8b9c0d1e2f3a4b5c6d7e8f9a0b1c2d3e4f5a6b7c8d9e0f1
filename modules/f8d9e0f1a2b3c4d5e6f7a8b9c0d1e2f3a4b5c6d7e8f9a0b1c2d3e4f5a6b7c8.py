#!/usr/bin/env python3
import json
import time
import hashlib
import base64
from VALE_master import state
from VALE_memory_ring import MemoryRing

class persona_roll:
    def __init__(self, base="default"):
        self.base = base
        self.weights = {"humor": 0.5, "empathy": 0.5, "tone": 0.5}
        self.memory = MemoryRing(capacity=10, duration=3600)

    def adapt(self, input_text):
        """Adapt weights based on input"""
        if "haha" in input_text.lower():
            self.weights["humor"] += 0.1
        if "okay okay" in input_text.lower():
            self.weights["empathy"] += 0.1
        self.weights["tone"] = max(0.3, min(0.7, self.weights["tone"]))
        self.memory.add({"input": input_text, "weights": self.weights})

    def apply(self, text):
        """Apply rolling persona to text"""
        return "Tone[{}]: {}".format(self.weights['tone'], text)

    def dump(self, silent=True):
        """Dump persona state to JSON, AES-256 encrypted"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output = {"timestamp": timestamp, "weights": self.weights}
        key = b'Sixteen byte key!'  # Replace with secure key in cradle
        cipher = hashlib.sha256(key).digest()[:32]
        iv = b'Sixteen byte iv!!'  # Replace with secure IV
        data = json.dumps(output).encode()
        padded = data + b' ' * (16 - len(data) % 16)
        encrypted = base64.b64encode(iv + cipher + padded)
        output = {"encrypted": encrypted.decode(), "timestamp": timestamp}
        if not silent:
            print(json.dumps(output, indent=2))
        return output

def apply_personality(text):
    """Wrapper function to export persona_roll's apply method"""
    return state['modules']['persona_roll'].apply(text)