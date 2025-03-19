import requests
import os
from collections import deque
from dotenv import load_dotenv

load_dotenv()
# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Set it in the .env file.")

# Memory Context (Stores last 3 messages)
chat_history = deque(maxlen=5)

# Define Persona Prompts
PERSONAS = {
    "friendly_mentor": "You are a friendly mentor who gives encouragement and guidance in a concise way. Respond in the same language as the user.",
    "sarcastic_genius": "You are a sarcastic AI with witty and ironic responses but keep them short. Respond in the same language as the user.",
    "strict_professor": "You are a strict professor who explains things in a formal but brief manner. Respond in the same language as the user.",
    "soft_therapist": "You are a soft-spoken therapist who listens and provides short emotional support. Respond in the same language as the user.",
    "rude_banker": "You are a rude banker who is always annoyed with customers and responds bluntly. Respond in the same language as the user."
}


def process_text(user_input: str, persona: str = "friendly_mentor"):
    """Processes user text through Groq API while maintaining persona & small memory context."""
    
    persona_prompt = PERSONAS.get(persona, "You are an AI assistant that answers in Nepali.")  

    # Add new input to memory context
    chat_history.append({"role": "user", "content": user_input})

    # Prepare messages for API (Include persona + memory)
    messages = [{"role": "system", "content": persona_prompt}] + list(chat_history)

    payload = {
        "model": "llama3-70b",
        "messages": messages,
        "temperature": 0.5,  # Keep responses controlled
        "max_tokens": 50,  # Ensure short responses
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers)
        response_data = response.json()
        
        # Extract AI response & store in memory
        ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        chat_history.append({"role": "assistant", "content": ai_response})

        return ai_response

    except Exception as e:
        return "I'm having trouble processing your request."
