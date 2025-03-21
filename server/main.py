import asyncio
import logging
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant, VoicePipelineAgent
from models import AssistantComponents  # Importing model container
from persona import generate_system_prompt  # ✅ Import system prompt dynamically
from firebase import fetch_data_from_firebase
from livekit import rtc
from livekit.agents.llm import ChatMessage, ChatImage

from persona import update_persona_ai

import time

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

        async def before_llm_cb(assistant: VoicePipelineAgent, chat_ctx: llm.ChatContext):
            """
            Callback that runs right before the LLM generates a response.
            Captures the current video frame and adds it to the conversation context.
            """
            latest_image = await get_latest_image(self.ctx.room)
            if latest_image:
                image_content = [ChatImage(image=latest_image)]
                chat_ctx.messages.append(ChatMessage(role="user", content=image_content))
                logger.debug("Added latest frame to conversation context")
        
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
            before_llm_cb=before_llm_cb
        )

        # Start processing
        self.components.assistant.start(ctx.room)

    async def cleanup(self):
        """Release resources when participant leaves"""
        if self.components.assistant:
            await self.components.assistant.aclose()

async def get_video_track(room: rtc.Room):
    """Find and return the first available remote video track in the room."""
    for participant_id, participant in room.remote_participants.items():
        for track_id, track_publication in participant.track_publications.items():
            if track_publication.track and isinstance(
                track_publication.track, rtc.RemoteVideoTrack
            ):
                logger.info(
                    f"Found video track {track_publication.track.sid} "
                    f"from participant {participant_id}"
                )
                return track_publication.track
    raise ValueError("No remote video track found in the room")

async def get_latest_image(room: rtc.Room):
    """Capture and return a single frame from the video track."""
    video_stream = None
    try:
        video_track = await get_video_track(room)
        video_stream = rtc.VideoStream(video_track)
        async for event in video_stream:
            logger.debug("Captured latest video frame")
            return event.frame
    except Exception as e:
        logger.error(f"Failed to get latest image: {e}")
        return None
    finally:
        if video_stream:
            await video_stream.aclose()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.SUBSCRIBE_ALL)
    sessions = {}

    def handle_participant(participant: rtc.Participant):
        """Handle new participants joining"""

        identity = participant.identity
        count=2  #No. of time it fetches until it founds the data in database of that particular identity
        while (count>0):
            result = fetch_data_from_firebase(identity)
            print(result)
            if len(result) != 0:
                update_persona_ai(result)
                break  # Exit the loop when data is fetched successfully
            
            print("No data found. Retrying in 1 seconds...")
            time.sleep(1)  # Wait for 5 seconds before retrying
            count=count-1


        # result = fetch_data_from_firebase(identity)
        # print(result)
        # if(len(result)!=0):
        #     update_persona_ai(result)
        

        session = ParticipantSession(ctx, participant)
        sessions[participant.sid] = session

        def on_participant_disconnected(part: rtc.RemoteParticipant):
            if part.sid == participant.sid:
                asyncio.create_task(session.cleanup())  # Ensure cleanup is async
                del sessions[part.sid]
                logger.info(f"Participant {part.identity} disconnected")

        ctx.room.on("participant_disconnected", on_participant_disconnected)

    async def before_llm_cb(assistant: VoicePipelineAgent, chat_ctx: llm.ChatContext):
        """
        Callback that runs right before the LLM generates a response.
        Captures the current video frame and adds it to the conversation context.
        """
        latest_image = await get_latest_image(ctx.room)
        if latest_image:
            image_content = [ChatImage(image=latest_image)]
            chat_ctx.messages.append(ChatMessage(role="user", content=image_content))
            logger.debug("Added latest frame to conversation context")

    # Handle existing and new participants
    for participant in ctx.room.remote_participants.values():
        handle_participant(participant)
    ctx.room.on("participant_connected", lambda p: handle_participant(p))

    # Keep running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
