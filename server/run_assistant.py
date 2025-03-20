import os
import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero
from models import initialize_stt, initialize_tts, initialize_llm 

# Load environment variables
load_dotenv()

# Read system prompt from file (or use a default)
SYSTEM_PROMPT_FILE = "system_prompt.txt"
try:
    with open(SYSTEM_PROMPT_FILE, 'r') as f:
        SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    SYSTEM_PROMPT = """You are Alex, a non-binary technical advisor known for extensive knowledge in programming and AI.
    You communicate in a friendly and informative manner.
    Your primary objective is to help users solve technical problems.
    You provide responses that are concise yet detailed, with practical examples.
    Your Backstory: Alex has 10 years of experience in software development and AI research."""

async def entrypoint(ctx: JobContext):
    """
    Main entrypoint for the LiveKit assistant.
    """
    print("🚀 Initializing LiveKit AI Assistant...")

    # Initialize STT, TTS, and LLM from models.py
    deepgram_stt = initialize_stt()
    deepgram_tts = initialize_tts()
    google_llm = initialize_llm()

    # Add system prompt to LLM Chat Context
    chat_context = llm.ChatContext().append(role="system", text=SYSTEM_PROMPT)

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
    # Run LiveKit AI Assistant
    worker_options = WorkerOptions(entrypoint_fnc=entrypoint)
    cli.run_app(worker_options)
