import os
import time
import hashlib
import json
from VALE_master import state

# Memory Management
def load_memory():
    """Load memory from disk"""
    if os.path.exists('vgu.mem'):
        with open('vgu.mem', 'r') as f:
            state['memory'] = json.load(f)
    else:
        state['memory'] = []

def save_memory():
    """Save memory to disk"""
    with open('vgu.mem', 'w') as f:
        json.dump(state['memory'], f)

def store_memory(data):
    """Store a single memory entry"""
    if len(state['memory']) >= state['modules']['sub']['memoryHandler']['storage']['maxEntries']:
        state['memory'].pop(0)
    state['memory'].append({
        'timestamp': time.time(),
        'data': data,
        'hash': hashlib.sha256(str(data).encode()).hexdigest()
    })
    if state['modules']['sub']['memoryHandler']['session']['autoSave']:
        save_memory()

def retrieve_memory(key):
    """Retrieve memory by key"""
    for entry in state['memory']:
        if entry['hash'] == key:
            return entry['data']
    return None

def get_context():
    """Get recent context for dialogue"""
    max_len = state['modules']['sub']['memoryHandler']['context']['maxContextLength']
    return state['memory'][-max_len:] if len(state['memory']) > max_len else state['memory']