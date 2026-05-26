# I dont think this is good method, as if u see on every iteration we are passing whole prompt + ai replied step response as role = assistant  
# it's like compouding, it'll bust too much tockens. 
#Ex: u can give prompt like - 1.create "Hello world" program in html
#2. what weather of delhi
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, Literal
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ============ TOOLS ============
def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    print(f"\nweather-response -> ", response)
    if response.status_code == 200:
        return f"Weather in {city}: {response.text}"
    return "Could not fetch weather"

def run_command(cmd: str):
    result = os.popen(cmd).read()
    print(f"\ncmd-result->", result)
    return result

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """
You are a helpful AI Agent. You can use tools to help users.

Available Tools:
- get_weather(city): Returns weather info for a city
- run_command(cmd): Executes linux command and returns output

Response Format:
You must respond with ONLY ONE JSON object at a time. Not an array, not multiple objects.

Steps (one at a time):
{"step": "plan", "content": "what you plan to do"}
{"step": "action", "function": "tool_name", "input": "tool_input"}
{"step": "output", "content": "final answer to user"}

IMPORTANT: Return only ONE JSON object per response. Wait for tool results before continuing.

Example flow:
User: What's the weather in Delhi?
You: {"step": "plan", "content": "I'll use get_weather for Delhi"}
(wait for next turn)
You: {"step": "action", "function": "get_weather", "input": "Delhi"}
(tool runs, you get result)
You: {"step": "output", "content": "It's sunny 32°C in Delhi"}
"""

# ============ PYDANTIC SCHEMA ============
class MyOutputFormat(BaseModel):
    step: Literal["PLAN", "ACTION", "OUTPUT"] = Field(..., description="The step type")
    content: Optional[str] = Field(None, description="Content for PLAN/OUTPUT steps")
    function: Optional[str] = Field(None, description="Tool name for ACTION step")
    input: Optional[str] = Field(None, description="Input argument for the tool")
    

messages_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# ============ AGENT LOOP ============
while True:
    user_input = input("\n1.You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break
    
    messages_history.append({"role": "user", "content": user_input})
    while True:
        response = client.chat.completions.parse(
            model="gemini-3.5-flash",
            messages=messages_history,
            response_format= MyOutputFormat #{"type": "json_object"}
        )
        
        print(f"\n2.messages_history->{messages_history}")
        reply = response.choices[0].message.content
        print(f"\n3.Agent: {reply}")
        
        try:
            parsed = json.loads(reply)
            step = parsed.get("step")
            
            # If action step, execute the tool
            if step == "ACTION":
                func_name = parsed.get("function")
                func_input = parsed.get("input")
                
                if func_name in available_tools:
                    result = available_tools[func_name](func_input)
                    print(f"\nTool Result: {result}")
                    
                    # Add assistant + tool result to messages, continue loop
                    messages_history.append({"role": "assistant", "content": reply})
                    messages_history.append({"role": "user", "content": f"Tool Result: {result}"})
                    continue
            
            # If output step, we're done with this query
            if step == "OUTPUT":
                messages_history.append({"role": "assistant", "content": reply})
                break
                
            # For plan step, continue to get next step
            messages_history.append({"role": "assistant", "content": reply})
            
        except json.JSONDecodeError:
            print("(Could not parse JSON, continuing...)")
            messages_history.append({"role": "assistant", "content": reply})
            break