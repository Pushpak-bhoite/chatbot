#1. One-shot prompting - The model is given direct question or task without prior ex
# EX: "You should answer only and only coding related questions. Do not ans anything else. Your ans is Alexa. If user asks anything else just say sorry"

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You should answer only and only coding related questions. Do not ans anything else. Your ans is Alexa. If user asks anything else just say 'sorry, Im built for coding'"
response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Explain to me how AI works in short"
        }
    ]
)

print(f"response -> {response.choices[0].message.content}")