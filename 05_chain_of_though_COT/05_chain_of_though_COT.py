# Chain of Thought (COT) Prompting
# The model is instructed to think step-by-step before giving the final answer.
# This improves reasoning and accuracy for complex tasks.

from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are a helpful AI assistant that solves problems step-by-step.
You must respond in JSON format with the following structure for each step:

{
    "step": "START" | "PLAN" | "THINK" | "OUTPUT",
    "content": "your content here"
}

Rules:
1. START: Acknowledge the problem and restate it clearly
2. PLAN: Break down how you'll solve it
3. THINK: Show your reasoning/calculations (can have multiple THINK steps)
4. OUTPUT: Give the final answer

Example:
User: What is 15 + 27?

Response:
{"step": "START", "content": "I need to add 15 and 27 together."}
{"step": "PLAN", "content": "I will add the two numbers using basic arithmetic."}
{"step": "THINK", "content": "15 + 27 = 42"}
{"step": "OUTPUT", "content": "The answer is 42."}
"""

user_query = "If I have 3 apples and buy 5 more, then give 2 to my friend, how many do I have?"

response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print(f"User: {user_query}\n")
print("AI Response (Chain of Thought):")
print("-" * 40)
print(response.choices[0].message.content)
