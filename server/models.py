import os
from dotenv import load_dotenv
from dataclasses import dataclass
from livekit.plugins import silero, openai, google
from persona import getPersona

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define voices for different personas
VOICE_MAP = {
    "male": "alloy",  # Example male voice
    "female": "nova",   # Example male voice
    "neutral": "echo"   # Example gender-neutral voice
}

@dataclass
class AssistantComponents:
    """Container for processing components per user"""
    vad: silero.VAD
    stt: openai.STT  # ✅ OpenAI Whisper for multilingual STT
    tts: openai.tts.TTS  # ✅ OpenAI TTS (Dynamically changes language & voice)
    llm: google.LLM
    assistant: object  # Placeholder for VoiceAssistant

    @staticmethod
    def create():
        """Factory method to create an instance with configured components."""
        # Determine voice based on persona sex
        persona = getPersona()
        voice = VOICE_MAP.get(persona.get("sex", "neutral").lower(), "echo")
        print(persona)

        return AssistantComponents(
            vad=silero.VAD.load(),
            stt=openai.STT(  
                model="whisper-1",
                api_key=OPENAI_API_KEY,
                language=None
            ),
            tts=openai.tts.TTS(  
                model="gpt-4o-mini-tts",
                voice=voice,  # ✅ Dynamically assigned voice
            ),
            llm=google.LLM(  
                model="gemini-2.0-flash",
                temperature=0.8,
                api_key=GOOGLE_API_KEY
            ),
            assistant=None  # Will be assigned later in main.py
        ) 