import json
import os
from typing import Dict, List, Optional
from VALE_storage import VALE_storage
from VALE_security import VALE_security
from VALE_persona import VALE_persona
from VALE_inputhandler import VALE_inputhandler
from VALE_memory import VALE_memory
from VALE_truthnet_core import VALE_truthnet_core
from VALE_truthnet_trace import VALE_truthnet_trace
from VALE_voice import VALE_voice
from VALE_rrs import VALE_rrs
from VALE_morality import VALE_morality

class VALE:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.storage = VALEStorage(self.config["endpoints"]["storage_api"], self.config["api_keys"]["storage"])
        self.security = VALESecurity(self.config["api_keys"])
        self.persona = VALEPersona(self.config["settings"]["default_personality"])
        self.input_handler = VALEInputHandler()
        self.memory = VALEMemory(self.config["settings"]["memory_retention_days"])
        self.truthnet_core = VALETruthNetCore()
        self.truthnet_trace = VALETruthNetTrace()
        self.rrs = VALERRS(self.config["weights"])
        self.morality = VALEMorality()
        self.voice = VALEVoice(self.config["settings"]["voice_enabled"])
        self.active = True

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError("Config file {0} not found".format(config_path))
        with open(config_path, 'r') as f:
            return json.load(f)

    def process_input(self, user_input: str, context: Optional[str] = None) -> str:
        """Process user input and generate response."""
        if not self.active:
            return "VALE is offline."
        
        # Secure and validate input
        sanitized_input = self.security.sanitize_input(user_input)
        if not sanitized_input:
            return "Invalid input detected."

        # Handle input
        intent = self.input_handler.parse_intent(sanitized_input)
        if intent["type"] == "query":
            # Truthnet core bomb and gauge
            bomb_results = self.truthnet_core.bomb_analysis(sanitized_input, context)
            gauge_output = self.truthnet_trace.trace_gauge(bomb_results)
            morality_response = self.morality.socratic_response(gauge_output, intent)
            response = morality_response
        elif intent["type"] == "command":
            response = self.execute_command(intent["command"], intent["args"])
        else:
            response = self.persona.generate_response(sanitized_input, context)

        # Store interaction in RRS via memory
        self.rrs.log_essence(sanitized_input, response, context)
        self.memory.store_interaction(sanitized_input, response, context)
        return response

    def format_response(self, gauge_output: Dict, intent: Dict) -> str:
        """Format gauge result into a response."""
        if gauge_output.get("error"):
            return "Error verifying fact: {0}".format(gauge_output['error'])
        return ("Claim: {0}\n".format(gauge_output['claim']) +
                "Truth Verdict: {0}\n".format(gauge_output['is_true']) +
                "Confidence: {0:.2f}%\n".format(gauge_output['confidence']*100) +
                "Sources: {0}".format(', '.join(gauge_output['sources'])))

    def execute_command(self, command: str, args: List) -> str:
        """Execute a system command."""
        if command == "shutdown":
            self.active = False
            return "VALE shutting down."
        elif command == "switch_personality":
            if args and args[0] in self.config["personalities"]:
                self.persona.load_personality(args[0])
                return "Personality switched to {0}.".format(args[0])
            return "Invalid personality specified."
        elif command == "voice_toggle":
            self.voice.toggle(args[0] if args else not self.config["settings"]["voice_enabled"])
            return "Voice {0}.".format("enabled" if self.voice.enabled else "disabled")
        return "Unknown command."

    def get_memory(self, query: str) -> Optional[Dict]:
        """Retrieve relevant memory for a query."""
        return self.memory.retrieve_relevant(query)
