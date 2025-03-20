import asyncio
import logging
from dataclasses import dataclass
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli,llm
from livekit.plugins import google, silero, turn_detector
from livekit.plugins.deepgram import stt, tts

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("multi_assistant")
import os
from dotenv import load_dotenv
load_dotenv()

# Hardcoded configuration (replace with your values)
DEEPGRAM_KEY = os.getenv("DEEPGRAM_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
LIVEKIT_KEY = os.getenv("LIVEKIT_API_KEY")

@dataclass
class AssistantComponents:
    """Container for processing components per user"""
    vad: silero.VAD
    stt: stt.STT
    tts: tts.TTS
    llm: google.LLM
    assistant: agents.voice_assistant.VoiceAssistant

class ParticipantSession:
    """Manages all resources for a single participant"""
    def __init__(self, ctx: JobContext, participant: rtc.Participant):
        self.ctx = ctx
        self.participant = participant
        
        # Initialize processing components
        self.components = AssistantComponents(
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
            assistant=None
        )

        # Create voice assistant
        self.components.assistant = agents.voice_assistant.VoiceAssistant(
            vad=self.components.vad,
            stt=self.components.stt,
            llm=self.components.llm,
            tts=self.components.tts,
            chat_ctx=llm.ChatContext(messages=[
            llm.ChatMessage(role="system", content="You are a helpful voice assistant.")
            ]),
            turn_detector=turn_detector.EOUModel()
        )

        # Start processing
        self.components.assistant.start(ctx.room)

    def _create_chat_context(self):
        return llm.ChatContext(messages=[{
            "role": "system",
            "content": "You are a helpful voice assistant. Keep responses brief and conversational."
        }])

    async def cleanup(self):
        """Release resources when participant leaves"""
        if self.components.assistant:
            await self.components.assistant.aclose()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)
    sessions = {}

    def handle_participant(participant: rtc.Participant):
        # Create session for new participant
        session = ParticipantSession(ctx, participant)
        sessions[participant.sid] = session

       

        def on_participant_disconnected(part: rtc.RemoteParticipant):
            if part.sid == participant.sid:
                session.cleanup()
                del sessions[part.sid]
                logger.info(f"Participant {part.identity} disconnected")

        # CORRECT WAY: Listen to room-level disconnect events
        ctx.room.on("participant_disconnected", on_participant_disconnected)

    # Handle existing and new participants
    for participant in ctx.room.remote_participants.values():
        handle_participant(participant)
    ctx.room.on("participant_connected", lambda p: handle_participant(p))

    # Keep running until cancelled
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))