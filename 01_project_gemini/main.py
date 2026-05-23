from google import genai
from dotenv import load_dotenv
import os

load_dotenv()  # reads variables from a .env file and sets them in os.environ

# Debug: Check if .env is loaded
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print(f"✅ API Key loaded: {api_key[:10]}...")  # Show first 10 chars only (for security)
else:
    print("❌ API Key NOT found! Check your .env path")

client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain how AI works in a few words, also tell me how are you buddy ?"
)

print("hello->", response.text)

