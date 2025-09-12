import hashlib
from typing import Dict, Optional

class VALESecurity:
    def __init__(self, api_keys: Dict):
        self.api_keys = api_keys

    def sanitize_input(self, input_text: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Basic sanitization for HTML/JS/SQL injection
        replacements = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            ';': '',
            '--': ''
        }
        sanitized = input_text
        for char, replacement in replacements.items():
            sanitized = sanitized.replace(char, replacement)
        return sanitized

    def hash_data(self, data: str) -> str:
        """Hash data for consistent identification."""
        return hashlib.sha256(data.encode()).hexdigest()

    def get_api_key(self, service: str) -> Optional[str]:
        """Retrieve API key for a service."""
        return self.api_keys.get(service)
