import os
import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero
from models import initialize_stt, initialize_tts, initialize_llm
from persona import generate_system_prompt  # ✅ Import system prompt dynamically

# Load environment variables
load_dotenv()

async def entrypoint(ctx: JobContext):
    """
    Main entrypoint for the LiveKit assistant.
    """
    print("🚀 Initializing LiveKit AI Assistant...")

    # Initialize STT, TTS, and LLM from models.py
    deepgram_stt = initialize_stt()
    deepgram_tts = initialize_tts()
    google_llm = initialize_llm()

    # Generate system prompt from the latest persona
    system_prompt = generate_system_prompt()
    print(system_prompt)
    chat_context = llm.ChatContext().append(role="system", text=system_prompt)

    # Create the AI Assistant
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram_stt,
        llm=google_llm,
        tts=deepgram_tts,
        chat_ctx=chat_context,  # ✅ Persona-based responses
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant.start(ctx.room)
    await asyncio.sleep(1)
    await assistant.say("Hey, how can I help you today!", allow_interruptions=True)

if __name__ == "__main__":
    worker_options = WorkerOptions(entrypoint_fnc=entrypoint)
    cli.run_app(worker_options)
