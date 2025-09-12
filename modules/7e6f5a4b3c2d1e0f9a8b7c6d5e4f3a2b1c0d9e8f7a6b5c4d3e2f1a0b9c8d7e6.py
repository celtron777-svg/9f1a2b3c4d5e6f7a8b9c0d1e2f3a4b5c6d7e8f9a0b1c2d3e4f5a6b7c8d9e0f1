class VALEVoice:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def toggle(self, enabled: bool) -> None:
        """Toggle voice output on or off."""
        self.enabled = enabled

    def speak(self, text: str) -> None:
        """Speak the given text if voice is enabled."""
        if self.enabled:
            # Placeholder for text-to-speech implementation
            print("[Voice Output]: " + text)
