from dotenv import load_dotenv
import os
from google.cloud import texttospeech

# Load environment variables from the .env file
load_dotenv()

# Now you can access the GOOGLE_APPLICATION_CREDENTIALS environment variable
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Verify the credentials path (optional)
if google_credentials_path:
    print(f"Credentials path loaded: {google_credentials_path}")
else:
    print("No credentials path set!")

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()

text="एक बार की बात है जब एक शेर जंगल में सो रहा था। उस समय एक चूहा उसके शरीर में उछल कूद करने लगा अपने मनोरंजन के लिए। इससे शेर की नींद ख़राब हो गयी और वो उठ गया साथ में गुस्सा भी हो गया।"

# Set the input text to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=text)

# Specify the voice parameters
voice = texttospeech.VoiceSelectionParams(
    language_code="hi-IN",
    name="hi-IN-Wavenet-A",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Set the audio configuration (MP3 format)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Request the speech synthesis
response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

# Save the audio content as an MP3 file
with open("response.mp3", "wb") as out:
    out.write(response.audio_content)


# from google.cloud import texttospeech
# from pydub import AudioSegment
# from pydub.playback import play
# from io import BytesIO

# def list_voices():
#     client = texttospeech.TextToSpeechClient()
#     response = client.list_voices()
#     for voice in response.voices:
#         print(f"Name: {voice.name}, Language: {voice.language_codes}, Gender: {voice.ssml_gender}")

# # list_voices()


# def speak_response(text, language_code="en-US", voice_name=None, gender="NEUTRAL"):
#     client = texttospeech.TextToSpeechClient()

#     synthesis_input = texttospeech.SynthesisInput(text=text)
    
#     # Configure the voice - Adjust language, name, and gender
#     voice_params = texttospeech.VoiceSelectionParams(
#         language_code=language_code,
#         name=voice_name,  
#         ssml_gender=getattr(texttospeech.SsmlVoiceGender, gender)
#     )

#     audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
#     response = client.synthesize_speech(
#         input=synthesis_input,
#         voice=voice_params,
#         audio_config=audio_config
#     )

#     audio_stream = BytesIO(response.audio_content)
#     print(audio_stream)
#     audio_segment = AudioSegment.from_file(audio_stream, format="mp3")
#     play(audio_segment)

# # Example Personalities
# speak_response("Hello! I am a humble actor.", language_code="en-GB", voice_name="en-GB-Wavenet-B", gender="MALE")
# speak_response("Hey! What do you want now?", language_code="en-US", voice_name="en-US-Wavenet-D", gender="MALE")
# speak_response("Bonjour! Je suis ici pour vous aider.", language_code="fr-FR", voice_name="fr-FR-Wavenet-A", gender="FEMALE")
