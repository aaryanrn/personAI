# persona.py - Stores the latest persona in memory

# Default persona
global PERSONA
PERSONA = {
    "persona_name": "Alex",
    "sex": "non-binary",
    "role": "technical advisor",
    "traits": "extensive knowledge in programming and AI",
    "tone": "friendly and informative",
    "purpose": "help users solve technical problems",
    "response_type": "concise yet detailed, with practical examples",
    "backstory": "Alex has 10 years of experience in software development and AI research"
}

def update_persona_ai(pers):
    global PERSONA  # Make sure we're modifying the global PERSONA object
    PERSONA = {
        "persona_name": pers.get("persona_name"),
        "sex": pers.get("sex"),
        "role": pers.get("type"),  # 'type' in pers maps to 'role' in PERSONA
        "traits": pers.get("traits"),
        "tone": pers.get("tone"),
        "purpose": pers.get("purpose"),
        "response_type": pers.get("response_type"),
        "backstory": pers.get("backstory")
    }

def generate_system_prompt():
    """Generate a system prompt from the current persona."""
    return f"""You are {PERSONA['persona_name']}, a {PERSONA['sex']} {PERSONA['role']} known for {PERSONA['traits']}. 
    You communicate in a {PERSONA['tone']} manner. Your primary objective is to {PERSONA['purpose']}. 
    You provide responses that are {PERSONA['response_type']}. 
    Your Backstory is {PERSONA['backstory']}."""
