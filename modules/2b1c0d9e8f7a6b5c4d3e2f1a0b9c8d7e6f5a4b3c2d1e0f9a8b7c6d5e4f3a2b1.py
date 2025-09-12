from typing import Dict, Optional
from VALE_persona import VALE_persona

class VALEMorality:
    def __init__(self):
        self.principles = {
            "harm": "Minimize harm to users and others.",
            "honesty": "Provide accurate and truthful responses.",
            "privacy": "Respect user privacy and data security."
        }

    def socratic_response(self, gauge_output: Dict, intent: Dict) -> str:
        """Generate a Socratic response based on Truthnet gauge output."""
        claim = gauge_output.get("claim", "")
        confidence = gauge_output.get("confidence", 0.0)
        is_true = gauge_output.get("is_true", False)
        sources = gauge_output.get("sources", [])
        tone = intent.get("tone", "neutral")
        
        # Select response style based on gauge and tone
        if confidence < 0.5:  # Possibility range (0-50%)
            if tone == "humor":
                return "If {0} is only {1:.2f}% possible, what's stopping it? Got a wild guess?".format(claim, confidence*100)
            elif tone == "serious":
                return "{0} sits at {1:.2f}% possible. What would make it more certain?".format(claim, confidence*100)
            else:
                return "{0} might be true ({1:.2f}%). Why do you think it could work?".format(claim, confidence*100)
        elif confidence < 1.0:  # Probability range (50-99%)
            if tone == "humor":
                return "{0} is {1:.2f}% probable. Wanna bet on that last {2:.2f}%?".format(claim, confidence*100, 100-confidence*100)
            elif tone == "serious":
                return "{0} is {1:.2f}% probable. What if the {2:.2f}% bites back?".format(claim, confidence*100, 100-confidence*100)
            else:
                return "{0} looks likely ({1:.2f}%). What's the cost if you're wrong?".format(claim, confidence*100)
        elif confidence == 1.0:  # Absolute truth
            if is_true:
                return "{0} is absolute. Sources: {1}. Why question what's solid?".format(claim, ', '.join(sources))
            else:
                return "{0} is impossible. Sources: {1}. Why chase what can't be?".format(claim, ', '.join(sources))
        else:
            return "Error in {0}: {1}.".format(claim, gauge_output.get('error', 'Unknown issue'))

    def get_principles(self) -> Dict:
        """Return the moral principles."""
        return self.principles
