from typing import Dict, Optional
from collections import deque
import time

class VALEMemoryRing:
    def __init__(self, max_size: int = 16000):
        self.memory = deque(maxlen=max_size)

    def store_interaction(self, input_text: str, response: str, context: Optional[str] = None, verbatim: bool = False) -> None:
        """Store an interaction in the ring buffer."""
        self.memory.append({
            "input": input_text,
            "response": response,
            "context": context,
            "timestamp": time.time(),
            "verbatim": verbatim
        })

    def retrieve_relevant(self, query: str) -> Optional[Dict]:
        """Retrieve the most recent relevant memory for a query."""
        for item in reversed(self.memory):
            if query.lower() in item["input"].lower():
                return item
        return None

    def clear(self) -> None:
        """Clear the memory ring."""
        self.memory.clear()
