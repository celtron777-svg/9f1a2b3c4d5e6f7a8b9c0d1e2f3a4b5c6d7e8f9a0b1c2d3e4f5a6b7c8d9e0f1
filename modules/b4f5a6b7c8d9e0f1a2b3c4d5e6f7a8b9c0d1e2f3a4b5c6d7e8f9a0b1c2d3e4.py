import json
from VALE_master import state
from VALE_morality import morality_check, handle_morality_error
from VALE_persona import persona_roll
from VALE_memory import get_context
from VALE_devtools import devtools_process

# Routing and Input Handling
def parse_input(text):
    """Parse user input for intent and content"""
    max_length = state['modules']['sub']['inputHandler']['maxInputLength']
    if len(text) > max_length:
        return {'error': 'Input too long', 'retry': True}
    intent = 'query'
    if text.startswith('switch '):
        intent = 'modeChange'
    elif text.startswith('!'):
        intent = 'command'
    return {
        'intent': intent,
        'content': text.strip(),
        'context': get_context()
    }

def route_input(parsed):
    """Route input to appropriate module"""
    if parsed['intent'] == 'modeChange':
        mode = parsed['content'].split(' ', 1)[1] if len(parsed['content'].split()) > 1 else ''
        if mode in state['modes']:
            state['mcf']['defaultMode'] = mode
            return "Switched to {} mode".format(mode)
        return "Invalid mode"
    elif parsed['intent'] == 'command':
        if parsed['content'].startswith('!dev'):
            command = parsed['content'].split(' ', 1)[1] if len(parsed['content'].split()) > 1 else ''
            return devtools_process(command)
        if parsed['content'] == '!status':
            return json.dumps(state, indent=2)
        elif parsed['content'] == '!backup':
            return create_backup()
        elif parsed['content'] == '!restore':
            return restore_backup()
    return generate_content(parsed['content'], parsed['context'])

# Content Generation
def generate_content(text, context):
    """Generate creative or conversational output"""
    mode = state['mcf']['defaultMode']
    if mode == 'Creative':
        if 'brainstorm' in text.lower():
            return "• Idea 1: {}\n• Idea 2: {} extended".format(text, text)
        elif 'story' in text.lower():
            return "Once upon a time, {} happened...".format(text)
        elif 'solution' in text.lower():
            return "Solution for {}: Try this approach.".format(text)
    elif mode == 'Banter':
        return "Hey, you said {}? That's wild!".format(text)
    elif mode == 'Discussion':
        return "Let's talk about {}. Here's my take...".format(text)
    return "Echo: {}".format(text)

# Task Management
def manage_tasks(task):
    """Coordinate tasks across modules"""
    queue = state['modules']['sub']['workflow']['taskQueue']
    tasks = [{'id': task, 'priority': 'high' if 'urgent' in task.lower() else 'normal'}]
    tasks.sort(key=lambda x: queue['priorityLevels'].index(x['priority']))
    
    for t in tasks:
        try:
            result = process_task(t['id'])
            state['modules']['sub']['feedbackLoop']['analysis']['metrics']['success'] = 0.95
            store_memory({'task': t['id'], 'result': result})
        except Exception as e:
            if state['modules']['sub']['workflow']['errorRecovery']['retryLimit'] > 0:
                state['modules']['sub']['workflow']['errorRecovery']['retryLimit'] -= 1
                return "Retrying task: {}".format(t['id'])
            return "Task failed: {}".format(str(e))

def process_task(task):
    """Execute a single task"""
    if 'generate' in task.lower():
        return generate_content(task, get_context())
    elif 'store' in task.lower():
        store_memory(task)
        return "Stored"
    return "Task processed"