import os
from livekit.plugins.deepgram import stt, tts
from livekit.plugins.google import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_stt():
    """Initialize Speech-to-Text (STT) using Deepgram."""
    return stt.STT(
        model="nova-2-general",
        interim_results=True,
        smart_format=True,
        punctuate=True,
        filler_words=True,
        profanity_filter=False,
        keywords=[("LiveKit", 1.5)],
        language="en-US",
        api_key=os.getenv("DEEPGRAM_API_KEY"),
    )

def initialize_tts():
    """Initialize Text-to-Speech (TTS) using Deepgram."""
    return tts.TTS(
        model="aura-angus-en",
        api_key=os.getenv("DEEPGRAM_API_KEY"),
    )

def initialize_llm():
    """Initialize LLM (Gemini 2.0) using Google API."""
    return LLM(
        model="gemini-2.0-flash",
        temperature=0.8,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )
