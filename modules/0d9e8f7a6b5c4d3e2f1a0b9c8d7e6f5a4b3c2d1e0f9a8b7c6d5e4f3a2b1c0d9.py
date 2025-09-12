import json
from typing import Optional
from VALE_morality import VALE_morality

class VALEPersona:
    def __init__(self, default_personality: str):
        self.current_personality = default_personality
        self.personalities = {}
        self.load_personality(default_personality)
        self.adaptive_mode = True

    def load_personality(self, personality_file: str) -> None:
        """Load a personality from a JSON file."""
        try:
            with open(personality_file, 'r') as f:
                personality_data = json.load(f)
            self.personalities[personality_file] = personality_data
            self.current_personality = personality_file
        except FileNotFoundError:
            raise FileNotFoundError("Personality file {0} not found".format(personality_file))

    def generate_response(self, input_text: str, context: Optional[str] = None, tone: str = "neutral") -> str:
        """Generate a response based on the current personality and tone."""
        personality = self.personalities.get(self.current_personality, {})
        base_tone = personality.get("tone", "neutral")
        
        # Adaptive persona switch for one-off responses
        if self.adaptive_mode and tone != "neutral":
            temp_personality = self._select_adaptive_personality(tone)
            if temp_personality:
                temp_data = self.personalities.get(temp_personality, personality)
                return "{0} response: {1} [{2}]".format(temp_data['tone'].capitalize(), input_text, temp_data['name'])
        
        return "{0} response: {1} [{2}]".format(base_tone.capitalize(), input_text, personality['name'])

    def _select_adaptive_personality(self, tone: str) -> Optional[str]:
        """Select a temporary personality based on detected tone."""
        tone_map = {
            "humor": "/home/celtron/vgu/personalities/VALE_personalities_cyberpunk.json",
            "serious": "/home/celtron/vgu/personalities/VALE_personalities_synthetics.json",
            "emotional": "/home/celtron/vgu/personalities/VALE_personalities_general.json"
        }
        return tone_map.get(tone)
