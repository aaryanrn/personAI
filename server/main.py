import asyncio
import time
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
    google,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit import rtc  # Add at the top
from firebase import fetch_data_from_firebase  # You must implement this
from persona import update_persona_ai, generate_system_prompt  # You must implement these

# Load .env variables
load_dotenv()

# Custom agent with dynamic instructions
class Assistant(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

# Entrypoint for the LiveKit Agent worker
async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()  # Required to start receiving participants

    async def handle_participant(participant: rtc.Participant):
        identity = participant.identity
        print(f"👤 Participant connected: {identity}")

        # 🔄 Try fetching Firebase data
        data = None
        for _ in range(3):
            data = fetch_data_from_firebase(identity)
            if data:
                update_persona_ai(data)  # Store persona details globally
                break
            print("⏳ No Firebase data found, retrying...")
            time.sleep(1)

        # 📜 Generate dynamic system prompt
        system_prompt = generate_system_prompt()
        print(f"📜 Using system prompt:\n{system_prompt}")

        # 🎙️ Setup voice AI session
        session = AgentSession(
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )

        await session.start(
            room=ctx.room,
            agent=Assistant(instructions=system_prompt),
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

        await session.generate_reply(
            instructions="Greet the user and offer your assistance."
        )

    # Handle participants who are already in the room
    for participant in ctx.room.remote_participants.values():
        asyncio.create_task(handle_participant(participant))

    # Handle participants who join later
    ctx.room.on("participant_connected", lambda p: asyncio.create_task(handle_participant(p)))

    # Keep the worker alive
    while True:
        await asyncio.sleep(1)

# CLI start
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
