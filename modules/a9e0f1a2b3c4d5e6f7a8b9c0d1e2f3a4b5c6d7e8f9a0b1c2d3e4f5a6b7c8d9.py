#!/usr/bin/env python3
import json
import time
import hashlib
import base64
from VALE_master import state
from VALE_memory_ring import MemoryRing

class rrs:
    def __init__(self, short_capacity=3, mid_capacity=10, mid_duration=3600):
        self.short = []  # Last 3 exchanges
        self.mid = MemoryRing(capacity=mid_capacity, duration=mid_duration)
        self.long = []   # Archival storage
        self.max_short = short_capacity

    def add(self, data):
        """Add to short-term, mid-term"""
        if len(self.short) >= self.max_short:
            self.short.pop(0)
        self.short.append({"data": data, "timestamp": time.time()})
        self.mid.add(data)
        self.long.append({"data": data, "timestamp": time.time()})

    def search(self, query):
        """Search all tiers by keyword"""
        results = []
        for tier in [self.short, self.mid.get(), self.long]:
            for entry in tier:
                if query.lower() in str(entry["data"]).lower():
                    results.append(entry)
        return results

    def rollback(self, n):
        """Rollback to nth last exchange"""
        if n < len(self.short):
            return self.short[-n]["data"]
        elif n < len(self.mid.get()):
            return self.mid.get()[-n]["data"]
        elif n < len(self.long):
            return self.long[-n]["data"]
        return None

    def dump(self, silent=True):
        """Dump to JSON, AES-256 encrypted"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output = {
            "timestamp": timestamp,
            "short": self.short,
            "mid": self.mid.get(),
            "long": self.long
        }
        key = b'Sixteen byte key!'  # Replace in cradle
        cipher = hashlib.sha256(key).digest()[:32]
        iv = b'Sixteen byte iv!!'  # Replace in cradle
        data = json.dumps(output).encode()
        padded = data + b' ' * (16 - len(data) % 16)
        encrypted = base64.b64encode(iv + cipher + padded)
        output = {"encrypted": encrypted.decode(), "timestamp": timestamp}
        if not silent:
            print(json.dumps(output, indent=2))
        return output