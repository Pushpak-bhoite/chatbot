
# it'll give current weather
import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner, WebSearchTool, set_tracing_disabled

load_dotenv()

# Disable tracing (requires OpenAI API key)
set_tracing_disabled(True)

# Create Gemini client using OpenAI-compatible endpoint
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

agent = Agent(
    name="History tutor",
    instructions="Hey Buddy, fetch current today's satara weather ",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=gemini_client,
    ),
    tools=[WebSearchTool] ### This is where we add tools, it could be Hosted tools, functions or etc. follow doc 
)



async def main() -> None:
    result = await Runner.run(agent, "When did the Roman Empire fall?")
    print("result==>\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
