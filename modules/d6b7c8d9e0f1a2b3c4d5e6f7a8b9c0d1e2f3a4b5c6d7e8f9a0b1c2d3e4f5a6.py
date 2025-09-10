#!/usr/bin/env python3
import json
import time
from VALE_master import state
import hashlib
import base64

class MemoryRing:
    def __init__(self, capacity=10, duration=3600):
        self.capacity = capacity  # Max 10 exchanges
        self.duration = duration  # 1-hour buffer
        self.buffer = []

    def add(self, data):
        """Add exchange to ring buffer"""
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append({"data": data, "timestamp": time.time()})

    def get(self, index=None):
        """Retrieve by index or all"""
        if index is not None:
            return self.buffer[index] if index < len(self.buffer) else None
        return self.buffer

    def flush(self, silent=True):
        """Flush to JSON, AES-256 stub"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        key = b'Sixteen byte key!'  # Replace in cradle
        cipher = hashlib.sha256(key).digest()[:32]
        iv = b'Sixteen byte iv!!'
        data = json.dumps(self.buffer).encode()
        padded = data + b' ' * (16 - len(data) % 16)
        encrypted = base64.b64encode(iv + cipher + padded)
        output = {"timestamp": timestamp, "encrypted": encrypted.decode()}
        if not silent:
            print(json.dumps(output, indent=2))
        return output