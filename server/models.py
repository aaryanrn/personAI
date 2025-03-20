import os
from livekit.plugins.openai import stt
from dotenv import load_dotenv
from livekit.plugins.google import LLM
from livekit.plugins import google

# Load environment variables
load_dotenv()

# Initialize STT (Speech-to-Text)
def initialize_stt():
    """Initialize Speech-to-Text using GROQ STT."""
    groq_stt = stt.STT.with_groq(
    model="whisper-large-v3-turbo",
    )
    
    return groq_stt

def initialize_tts():
    """Initialize Text-to-Speech using Cartesia TTS."""

    google_tts = google.TTS(
    gender="female",
    voice_name="en-US-Standard-H",
    )
    return google_tts

# Initialize LLM (Keep Google Gemini for now)
def initialize_llm():
    """Initialize LLM (Gemini 2.0) using Google API."""
    return LLM(
        model="gemini-2.0-flash",
        temperature=0.8,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )
