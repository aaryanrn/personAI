import os
import requests
from dotenv import load_dotenv
from langdetect import detect
from collections import deque

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    print("❌ Error: API key not found. Make sure you have a valid `.env` file.")
    exit(1)

# Define Persona Prompts
PERSONAS = {
    "friendly_mentor": "You are a friendly mentor who gives encouragement and guidance.",
    "sarcastic_genius": "You are a sarcastic AI with witty and ironic responses but keep them short.",
    "strict_professor": "You are a strict professor who explains things in a formal but brief manner.",
    "soft_therapist": "You are a soft-spoken therapist who listens and provides short emotional support.",
    "rude_banker": "You are a rude banker who is always annoyed with customers and responds bluntly."
}

# Chat History (Stores last 4 exchanges)
chat_history = deque(maxlen=4)  # Stores last 4 user-AI messages

def detect_language(text):
    """Detect the user's language from the input text."""
    try:
        return detect(text)
    except:
        return "en"  # Default to English if detection fails

def get_system_prompt(persona="friendly_mentor"):
    """Returns the system prompt with persona definition."""
    return {
        "role": "system",
        "content": f"{PERSONAS.get(persona, 'You are an AI assistant.')}\n"
                   "Your job is to provide clear and concise responses while staying in character.\n"
                   "Always respond in the same language as the user.\n"
                   "Do not break character under any circumstance.\n"
                   "Maintain a small memory of the conversation but prioritize keeping responses short."
    }

def chat_with_ai(user_input, persona="friendly_mentor"):
    """Process user input while keeping a rotating system prompt + last 4 messages."""

    detected_lang = detect_language(user_input)

    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Prepare messages for API (Always include system prompt + last 4 messages)
    messages = [get_system_prompt(persona)] + list(chat_history)

    payload = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 100
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers)
        response_data = response.json()

        # Extract AI response & store in memory
        ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        chat_history.append({"role": "assistant", "content": ai_response})

        return ai_response  # Returning response for external usage (e.g., TTS)

    except Exception as e:
        return f"❌ API Error: {str(e)}"

# Start Chat
print("🎭 Chat with your AI Persona! (Type 'exit' to stop)")
selected_persona = input("Choose a persona (friendly_mentor, sarcastic_genius, strict_professor, soft_therapist, rude_banker): ").strip()

while True:
    user_text = input("You: ")
    if user_text.lower() == "exit":
        print("👋 Exiting chat...")
        break
    
    ai_response = chat_with_ai(user_text, selected_persona)
    
    print(f"🤖 AI ({selected_persona}): {ai_response}")

    # Send response to another function (e.g., Text-to-Speech)
    # convert_to_speech(ai_response)  # Uncomment this if integrating ttS
