import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/models"

if not GROQ_API_KEY:
    print("❌ Error: API key not found. Check your .env file.")
    exit(1)

headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

try:
    response = requests.get(GROQ_ENDPOINT, headers=headers)
    response_data = response.json()
    print("✅ Available models on Groq API:")
    for model in response_data.get("data", []):
        print(f"🔹 {model['id']}")
except Exception as e:
    print(f"❌ Error fetching models: {str(e)}")
