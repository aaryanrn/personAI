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

# Set the input text to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="एक बार की बात है जब एक शेर जंगल में सो रहा था। उस समय एक चूहा उसके शरीर में उछल कूद करने लगा अपने मनोरंजन के लिए। इससे शेर की नींद ख़राब हो गयी और वो उठ गया साथ में गुस्सा भी हो गया।")

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

