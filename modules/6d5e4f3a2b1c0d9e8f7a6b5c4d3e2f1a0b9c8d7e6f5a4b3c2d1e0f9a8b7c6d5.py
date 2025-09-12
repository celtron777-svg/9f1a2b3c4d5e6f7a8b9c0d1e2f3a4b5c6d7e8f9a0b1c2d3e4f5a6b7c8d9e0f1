from typing import Dict, Optional
import time
from datetime import datetime, timedelta
from VALE_storage import VALE_storage

class VALEMemory:
    def __init__(self, retention_days: int):
        self.memory = {}
        self.retention_days = retention_days
        self.storage = VALEStorage("https://api.storage.vale.org/v1", "st_api_0987654321fedcba")

    def store_interaction(self, input_text: str, response: str, context: Optional[str] = None, verbatim: bool = False) -> None:
        """Store an interaction in memory or as a verbatim note."""
        timestamp = time.time()
        entry = {
            "response": response,
            "context": context,
            "timestamp": timestamp,
            "verbatim": verbatim
        }
        self.memory[input_text] = entry
        if verbatim:
            self.storage.save_verbatim_note(input_text, entry)
        self._prune_old_memories()

    def retrieve_relevant(self, query: str) -> Optional[Dict]:
        """Retrieve the most relevant memory for a query."""
        for input_text, data in self.memory.items():
            if query.lower() in input_text.lower():
                return data
        return self.storage.get_verbatim_note(query)

    def _prune_old_memories(self) -> None:
        """Remove memories older than retention period, except verbatim notes."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        cutoff_timestamp = cutoff.timestamp()
        self.memory = {k: v for k, v in self.memory.items() if v["timestamp"] >= cutoff_timestamp or v["verbatim"]}
