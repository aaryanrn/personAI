import asyncio
import logging
import time
import types
from functools import lru_cache
from dotenv import load_dotenv
from langdetect import detect
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant, VoicePipelineAgent
from livekit.agents.llm import ChatMessage, ChatImage
from models import AssistantComponents
from persona import generate_system_prompt, update_persona_ai, PERSONA
from firebase import fetch_data_from_firebase

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("multi_assistant")

# Supported TTS languages
LANGUAGE_MAP = {
    "en": ("en-US", "en-US-Standard-H"),
    "hi": ("hi-IN", "hi-IN-Standard-A"),
    "es": ("es-ES", "es-ES-Standard-A"),
    "fr": ("fr-FR", "fr-FR-Standard-A"),
    "de": ("de-DE", "de-DE-Standard-A"),
    "zh-cn": ("zh-CN", "cmn-CN-Standard-A"),
    "ar": ("ar-XA", "ar-XA-Standard-A"),
    "ja": ("ja-JP", "ja-JP-Standard-A"),
    "sw": ("hi-IN", "hi-IN-Standard-A"),
}

def detect_language(text):
    """Detects the language from transcribed text with error handling."""
    try:
        logger.info(f"🔍 Detecting language from text: {text[:50]}...")
        lang_code = detect(text)
        logger.info(f"🎂 Detected language: {lang_code}")
        return LANGUAGE_MAP.get(lang_code, LANGUAGE_MAP["en"])
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return LANGUAGE_MAP["en"]

async def async_gen_to_str(async_gen):
    """Converts an async generator into a single string."""
    result = []
    async for item in async_gen:
        result.append(str(item))
    return " ".join(result)

class ParticipantSession:
    """Manages all resources for a single participant."""
    
    def __init__(self, ctx: JobContext, participant: rtc.Participant):
        self.ctx = ctx
        self.participant = participant
        self.components = AssistantComponents.create(PERSONA)
        self.last_detected_lang = "en"
        self.last_detected_voice = "en-US-Standard-H"

        system_prompt = generate_system_prompt()
        logger.info(f"System Prompt: {system_prompt}")

        async def before_llm_cb(assistant: VoicePipelineAgent, chat_ctx: llm.ChatContext):
            """Callback before LLM generates a response - adds video frames."""
            latest_image = await get_latest_image(self.ctx.room)
            if latest_image:
                chat_ctx.messages.append(ChatMessage(role="user", content=[ChatImage(image=latest_image)]))
                logger.debug("Added latest video frame to conversation")

        self.chat_context = llm.ChatContext().append(role="system", text=system_prompt)
        self.components.assistant = VoiceAssistant(
            vad=self.components.vad,
            stt=self.components.stt,
            llm=self.components.llm,
            tts=self.components.tts,
            chat_ctx=self.chat_context,
            before_llm_cb=before_llm_cb,
            # before_tts_cb=self.before_tts_cb
        )
        self.components.assistant.start(ctx.room)

    async def cleanup(self):
        """Release resources when participant leaves."""
        if self.components.assistant:
            await self.components.assistant.aclose()

    @lru_cache(maxsize=10)
    def detect_language_cached(self, text):
        """Cached version of language detection to prevent redundant computations."""
        return detect_language(text)

    async def before_tts_cb(self, assistant, transcribed_text):
        """Dynamically updates the TTS language based on detected STT language."""
        if isinstance(transcribed_text, types.AsyncGeneratorType):
            transcribed_text = await async_gen_to_str(transcribed_text)

        transcribed_text = transcribed_text.strip()
        if not transcribed_text:
            return transcribed_text

        lang, voice = self.detect_language_cached(transcribed_text[:100])  # Use only first 100 chars

        if lang != self.last_detected_lang:
            self.last_detected_lang = lang
            self.last_detected_voice = voice
            self.components.tts.language = lang
            self.components.tts.voice_name = voice
            logger.info(f"🔄 Updated TTS to Language: {self.components.tts.language}, Voice: {self.components.tts.voice_name}")

        return transcribed_text
    
async def get_video_track(room: rtc.Room):
    """Find and return the first available remote video track in the room."""
    for participant in room.remote_participants.values():
        for track_publication in participant.track_publications.values():
            if track_publication.track and isinstance(track_publication.track, rtc.RemoteVideoTrack):
                logger.info(f"Found video track {track_publication.track.sid} from participant {participant.identity}")
                return track_publication.track
    raise ValueError("No remote video track found in the room")

async def get_latest_image(room: rtc.Room):
    """Capture and return a single frame from the video track."""
    try:
        video_track = await get_video_track(room)
        video_stream = rtc.VideoStream(video_track)
        async for event in video_stream:
            logger.debug("Captured latest video frame")
            return event.frame
    except Exception as e:
        logger.error(f"Failed to get latest image: {e}")
        return None

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the voice assistant."""
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.SUBSCRIBE_ALL)
    sessions = {}

    def handle_participant(participant: rtc.Participant):
        """Handle new participants joining."""
        identity = participant.identity
        count = 2
        while count > 0:
            result = fetch_data_from_firebase(identity)
            if result:
                update_persona_ai(result)
                break
            logger.info("No data found. Retrying in 1 second...")
            time.sleep(1)
            count -= 1

        session = ParticipantSession(ctx, participant)
        sessions[participant.sid] = session

        def on_participant_disconnected(part: rtc.RemoteParticipant):
            if part.sid == participant.sid:
                asyncio.create_task(session.cleanup())
                del sessions[part.sid]
                logger.info(f"Participant {part.identity} disconnected")

        ctx.room.on("participant_disconnected", on_participant_disconnected)

    for participant in ctx.room.remote_participants.values():
        handle_participant(participant)
    ctx.room.on("participant_connected", lambda p: handle_participant(p))

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
