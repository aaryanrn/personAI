import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, google, cartesia
from livekit.plugins.openai import stt
# from api import AssistantFnc
from livekit.plugins.deepgram import tts

load_dotenv()

deepgram_tts = tts.TTS(
    model="aura-asteria-en",
    api_key=os.getenv("DEEPGRAM_API_KEY"),
)
# google_tts = google.TTS(
#   gender="female",
#   voice_name="en-US-Standard-H",
# )

google_llm = google.LLM(
  model="gemini-2.0-flash",
  temperature="0.8",
  api_key=os.getenv("GOOGLE_API_KEY")
)

# deepgram_stt = stt.STT(
#     model="nova-3",
#     interim_results=True,
#     detect_language=True,
#     smart_format=True,
#     punctuate=True,
#     filler_words=True,
#     profanity_filter=False,
#     language="en-US",
#     api_key=os.getenv("DEEPGRAM_API_KEY"),
# )
# google_stt = google.STT(
# #   model="chirp",
#   spoken_punctuation=False,

# )



groq_stt = stt.STT.with_groq(
  model="whisper-large-v3-turbo",
  detect_language=True,
  language="en",
)

rude = "Be extremely rude while answering any queries"
name   = "Vson"
async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            f"""You are a voice assistant created by {name}. Your interface with users will be voice. 
            You should use short and concise responses, and avoiding usage of unpronouncable punctuation.
            """
            #"You should answer questions and provide information in French Language"
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    #fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=groq_stt,
        llm=google_llm,
        tts=deepgram_tts,
        chat_ctx=initial_ctx,
        #fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
