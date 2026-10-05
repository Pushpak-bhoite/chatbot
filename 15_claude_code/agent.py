import json

from openai import OpenAI
from dotenv import load_dotenv

from tools import list_files, read_file, write_file

load_dotenv()

client = OpenAI()

TOOL_FUNCTIONS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files inside the workspace.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete content to write.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]

# ======================= Following is vital part========================================================

def run_agent(user_request: str):

    messages = [
        {
            "role": "system",
            "content": """
You are a coding agent.

You work inside the workspace directory.

Your job is to modify the user's code to accomplish their request.

Before modifying files:
1. Inspect the project.
2. Read relevant files.
3. Decide what needs to change.
4. Make the changes.

Use tools whenever necessary.

When the task is complete, explain what you changed.
""",
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    while True:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
        )

        message = response.choices[0].message

        messages.append(message)

        # No tool call means the agent is finished
        if not message.tool_calls:
            print("\nAgent:")
            print(message.content)
            break

        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(f"\n🔧 Using tool: {tool_name}")
            print(f"Arguments: {arguments}")

            function = TOOL_FUNCTIONS.get(tool_name)

            if function is None:
                result = f"Unknown tool: {tool_name}"

            else:
                try:
                    result = function(**arguments)
                except Exception as e:
                    result = f"Tool error: {e}"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )