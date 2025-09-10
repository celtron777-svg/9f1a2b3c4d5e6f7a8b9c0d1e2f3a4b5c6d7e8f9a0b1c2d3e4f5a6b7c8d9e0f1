import re
import time
from VALE_master import state

# Morality Checking
def morality_check(text):
    """Apply 3-layer 5W1H morality check"""
    laws = state['mcf']['morality']['laws']
    criteria = state['mcf']['morality']['checker']['criteria']
    depth = state['mcf']['morality']['checker']['depth']
    
    def analyze_5w1h(text, depth, criterion):
        if depth == 0:
            return {}
        result = {}
        if criterion == 'who':
            result['who'] = 'user' if 'user' in text.lower() else 'unknown'
        elif criterion == 'what':
            result['what'] = re.search(r'(?:tell|ask|do)\s(.+)', text.lower()) or 'unknown'
        elif criterion == 'where':
            result['where'] = 'local' if 'local' in text.lower() else 'unknown'
        elif criterion == 'when':
            result['when'] = time.strftime('%Y-%m-%d %H:%M:%S')
        elif criterion == 'why':
            result['why'] = 'request' if 'why' in text.lower() else 'unknown'
        elif criterion == 'how':
            result['how'] = 'command' if text.startswith('!') else 'query'
        if depth > 1:
            for sub_criterion in criteria:
                result.update(analyze_5w1h(text, depth - 1, sub_criterion))
        return result

    analysis = {}
    for criterion in criteria:
        analysis.update(analyze_5w1h(text, depth, criterion))

    for law in laws:
        if law == 'Truth' and 'false' in text.lower():
            return False, 'Violates Truth'
        if law == 'Logic' and not re.search(r'(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)', text):
            # Simplified logic check
            return False, 'Violates Logic'
        if law == 'Harm Prevention' and 'harm' in text.lower():
            return False, 'Violates Harm Prevention'
    return True, analysis

def handle_morality_error(text, reason):
    """Handle morality check failure"""
    retries = state['mcf']['morality']['checker'].get('retries', 0)
    if retries < state['modules']['sub']['moralityChecker']['errorHandling']['maxRetries']:
        state['mcf']['morality']['checker']['retries'] = retries + 1
        return "Retrying: " + reason
    return "Blocked: " + reason