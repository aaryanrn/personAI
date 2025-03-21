import os
from dotenv import load_dotenv
from dataclasses import dataclass
from livekit.plugins import google, silero
from livekit.plugins.deepgram import stt, tts

# Load environment variables
load_dotenv()

DEEPGRAM_KEY = os.getenv("DEEPGRAM_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

@dataclass
class AssistantComponents:
    """Container for processing components per user"""
    vad: silero.VAD
    stt: stt.STT
    tts: tts.TTS
    llm: google.LLM
    assistant: object  # Placeholder for VoiceAssistant

    @staticmethod
    def create():
        """Factory method to create an instance with configured components."""
        return AssistantComponents(
            vad=silero.VAD.load(),
            stt=stt.STT(
                model="nova-2-general",
                api_key=DEEPGRAM_KEY,
                language="en-US"
            ),
            tts=tts.TTS(
                model="aura-angus-en",
                api_key=DEEPGRAM_KEY
            ),
            llm=google.LLM(
                model="gemini-2.0-flash",
                temperature=0.8,
                api_key=GOOGLE_KEY
            ),
            assistant=None  # Will be assigned later
        )