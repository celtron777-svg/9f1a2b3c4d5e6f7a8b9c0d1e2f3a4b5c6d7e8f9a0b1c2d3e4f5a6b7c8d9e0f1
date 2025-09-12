from typing import List, Dict, Optional
import time

class VALERRS:
    def __init__(self, weights_files: List[str]):
        self.weights = self.load_weights(weights_files)
        self.conversation_log = []

    def load_weights(self, weights_files: List[str]) -> Dict:
        """Load weights from text files or generate dummy data if missing."""
        weights = {}
        for file in weights_files:
            try:
                with open(file, 'r') as f:
                    weights[file] = [float(line) for line in f.readlines()]
            except FileNotFoundError:
                # Generate dummy weights for testing
                print("Weights file " + file + " not found, using dummy data")
                weights[file] = [0.5] * 100  # 100 floats for placeholder
        return weights

    def log_essence(self, input_text: str, response: str, context: Optional[str] = None, verbatim: bool = False) -> None:
        """Log the essence or verbatim note of a conversation."""
        entry = {
            "input": input_text,
            "response": response,
            "context": context,
            "timestamp": time.time(),
            "verbatim": verbatim
        }
        self.conversation_log.append(entry)

    def retrieve_conversation(self, query: str) -> Optional[Dict]:
        """Retrieve a conversation entry based on a query."""
        for entry in reversed(self.conversation_log):
            if query.lower() in entry["input"].lower():
                return entry
        return None
