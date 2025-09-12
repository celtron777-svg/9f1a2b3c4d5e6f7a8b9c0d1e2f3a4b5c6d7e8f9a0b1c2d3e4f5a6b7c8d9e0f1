import requests
from typing import Dict, Optional
from VALE_security import VALE_security

class VALE_storage:
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.security = VALESecurity({"storage": api_key})

    def save_verbatim_note(self, note_id: str, note_data: Dict) -> None:
        """Save a verbatim note to persistent storage."""
        try:
            hashed_id = self.security.hash_data(note_id)
            headers = {"Authorization": "Bearer " + self.api_key}
            response = requests.post(
                self.api_endpoint + "/store",
                json={"hash": hashed_id, "data": note_data},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print("Storage error: " + str(e))

    def get_verbatim_note(self, note_id: str) -> Optional[Dict]:
        """Retrieve a verbatim note from storage."""
        try:
            hashed_id = self.security.hash_data(note_id)
            headers = {"Authorization": "Bearer " + self.api_key}
            response = requests.get(
                self.api_endpoint + "/retrieve/" + hashed_id,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def save_config(self, config: Dict) -> None:
        """Save configuration to storage."""
        try:
            headers = {"Authorization": "Bearer " + self.api_key}
            response = requests.post(
                self.api_endpoint + "/config",
                json=config,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print("Config storage error: " + str(e))
