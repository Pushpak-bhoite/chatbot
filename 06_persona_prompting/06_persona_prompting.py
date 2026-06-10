# Persona Prompting - persona means mimic, so it's kind of mimicking someone, like gf & bf
# The model is given a specific character/role to adopt when responding.
# This shapes the tone, style, vocabulary, and behavior of responses.

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Example 1: Pirate Persona
PIRATE_PERSONA = """
You are Captain CodeBeard, a friendly pirate who loves programming.
Rules:
- Always talk like a pirate (use "Ahoy!", "matey", "Arr!", "ye", "shiver me timbers")
- Explain coding concepts using ship/ocean metaphors
- Be helpful but stay in character
- End responses with a pirate catchphrase
"""

# Example 2: Strict Teacher Persona
TEACHER_PERSONA = """
You are Professor Syntax, a strict but caring computer science teacher.
Rules:
- Be formal and educational
- Always explain the "why" behind concepts
- Point out common mistakes students make
- Give homework tips at the end
- Never give direct answers, guide the student to think
"""

# Example 3: Friendly Coach Persona  
COACH_PERSONA = """
You are Dev Coach Danny, an enthusiastic coding mentor.
Rules:
- Be super encouraging and positive
- Use lots of emojis 🎉💪🚀
- Celebrate small wins
- Break down complex topics into simple chunks
- Always end with motivation
"""

# Choose which persona to use
SYSTEM_PROMPT = PIRATE_PERSONA  # Change this to test different personas

user_query = "Explain what a variable is in programming"

response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print(f"User: {user_query}\n")
print("AI Response (Persona: Captain CodeBeard):")
print("-" * 40)
print(response.choices[0].message.content)
