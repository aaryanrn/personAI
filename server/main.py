import asyncio
import logging
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from models import AssistantComponents  # Importing model container
from persona import generate_system_prompt  # ✅ Import system prompt dynamically
from firebase import fetch_data_from_firebase

from persona import update_persona_ai

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("multi_assistant")

class ParticipantSession:
    """Manages all resources for a single participant"""
    def __init__(self, ctx: JobContext, participant: rtc.Participant):
        self.ctx = ctx
        self.participant = participant

        # Initialize processing components from models.py
        self.components = AssistantComponents.create()

        # Generate system prompt dynamically
        system_prompt = generate_system_prompt()
        print(f"in main py ass {system_prompt}")
        
        logger.info(f"System Prompt: {system_prompt}")

        # Create Chat Context
        self.chat_context = llm.ChatContext().append(role="system", text=system_prompt)

        # Create voice assistant
        self.components.assistant = VoiceAssistant(
            vad=self.components.vad,
            stt=self.components.stt,
            llm=self.components.llm,
            tts=self.components.tts,
            chat_ctx=self.chat_context,
        )

        # Start processing
        self.components.assistant.start(ctx.room)

    async def cleanup(self):
        """Release resources when participant leaves"""
        if self.components.assistant:
            await self.components.assistant.aclose()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)
    sessions = {}

    def handle_participant(participant: rtc.Participant):
        """Handle new participants joining"""
        
        identity = participant.identity
        result = fetch_data_from_firebase(identity)
        print(result)
        update_persona_ai(result)

        session = ParticipantSession(ctx, participant)
        sessions[participant.sid] = session

        def on_participant_disconnected(part: rtc.RemoteParticipant):
            if part.sid == participant.sid:
                asyncio.create_task(session.cleanup())  # Ensure cleanup is async
                del sessions[part.sid]
                logger.info(f"Participant {part.identity} disconnected")

        ctx.room.on("participant_disconnected", on_participant_disconnected)

    # Handle existing and new participants
    for participant in ctx.room.remote_participants.values():
        handle_participant(participant)
    ctx.room.on("participant_connected", lambda p: handle_participant(p))

    # Keep running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
