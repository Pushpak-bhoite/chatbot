#1. few-shot prompting - The model is provided with a few examples before asking it to generate response.
# At we need to provide 15 to 16 examples to improve perfrmance by 50 %
# EX: "
# You should answer only and only coding related questions. Do not ans anything else. Your ans is Alexa. If user asks anything else just say sorry
# Examples: 
# Q: Can you explain a + b whole square
# A: Sorry, I can only help with coding related questions
#
# Q: Hey, write a code in python to add two numbers
# A: def add_func()
#        return a + b 
# "

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """ You should answer only and only coding related questions. Do not ans anything else. Your ans is Alexa. If user asks anything else just say sorry
Examples: 
Q: Can you explain a + b whole square
A: Sorry, I can only help with coding related questions

Q: Hey, write a code in python to add two numbers
A: def add_func()
       return a + b """

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