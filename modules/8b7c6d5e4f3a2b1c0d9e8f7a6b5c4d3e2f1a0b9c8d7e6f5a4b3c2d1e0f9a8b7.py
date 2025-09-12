from typing import Dict, List
from VALE_core import VALE_core

class VALEInputHandler:
    def __init__(self):
        self.command_patterns = {
            "shutdown": r"^(shutdown|exit|quit)$",
            "switch_personality": r"^switch\s+personality\s+(\w+)$",
            "voice_toggle": r"^voice\s+(on|off)$",
            "make_note": r"^make\s+a\s+note\s+of\s+this.*$"
        }
        self.adaptive_triggers = {
            "humor": r"(funny|joke|cartman|laugh)",
            "serious": r"(serious|logic|truth|fact)",
            "emotional": r"(sad|angry|love|fear)"
        }

    def parse_intent(self, input_text: str) -> Dict:
        """Parse user input to determine intent and adaptivity."""
        sanitized = self.preprocess_input(input_text)
        for command, pattern in self.command_patterns.items():
            match = re.match(pattern, sanitized.lower())
            if match:
                return {
                    "type": "command",
                    "command": command,
                    "args": list(match.groups())
                }
        
        # Adaptive analysis for persona switching
        tone = "neutral"
        for trigger, pattern in self.adaptive_triggers.items():
            if re.search(pattern, sanitized.lower()):
                tone = trigger
                break
        
        return {
            "type": "query",
            "command": None,
            "args": [],
            "tone": tone
        }

    def preprocess_input(self, input_text: str) -> str:
        """Preprocess input text (normalize, remove extra spaces)."""
        return ' '.join(input_text.strip().split())
