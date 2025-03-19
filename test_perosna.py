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

# Define Persona Prompts with Multilingual Support
PERSONAS = {
    "friendly_mentor": "You are a friendly mentor who gives encouragement and guidance.",
    "sarcastic_genius": "You are a sarcastic AI with witty and ironic responses but keep them short.",
    "strict_professor": "You are a strict professor who explains things in a formal but brief manner.",
    "soft_therapist": "You are a soft-spoken therapist who listens and provides short emotional support.",
    "rude_banker": "You are a rude banker who is always annoyed with customers and responds bluntly."
}

# Chat History (Stores last 5 exchanges)
chat_history = deque(maxlen=5)

def detect_language(text):
    """Detect the user's language from the input text."""
    try:
        return detect(text)
    except:
        return "en"  # Default to English if detection fails

def initialize_chat(persona="friendly_mentor"):
    """Set up the system prompt at the start of the conversation."""
    detected_lang = "en"  # Default language; will adjust based on user input
    system_prompt = (
        f"{PERSONAS.get(persona, 'You are an AI assistant.')}\n"
        f"Your job is to provide clear and concise responses while staying in character.\n"
        f"Always respond in the same language as the user.\n"
        f"Do not break character under any circumstance.\n"
        f"Maintain a small memory of the conversation but prioritize keeping responses short."
    )
    # Initialize chat history with system prompt
    chat_history.append({"role": "system", "content": system_prompt})

def chat_with_ai(user_input):
    """Process user input while keeping chat context (Last 5 messages)."""

    detected_lang = detect_language(user_input)

    # Add new user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Prepare messages for API (System Prompt + Memory Context)
    messages = list(chat_history)

    payload = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.5,  # Keep responses controlled
        "max_tokens": 100  # Ensure short responses
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers)
        response_data = response.json()

        # Extract AI response & store in memory
        ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        chat_history.append({"role": "assistant", "content": ai_response})

        return ai_response  # Returning response for external usage

    except Exception as e:
        return f"❌ API Error: {str(e)}"

# Start Chat
print("🎭 Chat with your AI Persona! (Type 'exit' to stop)")
selected_persona = input("Choose a persona (friendly_mentor, sarcastic_genius, strict_professor, soft_therapist, rude_banker): ").strip()

# Initialize chat with a persistent system prompt
initialize_chat(selected_persona)

while True:
    user_text = input("You: ")
    if user_text.lower() == "exit":
        print("👋 Exiting chat...")
        break
    
    ai_response = chat_with_ai(user_text)
    
    print(f"🤖 AI ({selected_persona}): {ai_response}")

    # Send response to another function (e.g., Text-to-Speech)
    # Here, replace `convert_to_speech(ai_response)` with your friend's function
    # convert_to_speech(ai_response)
