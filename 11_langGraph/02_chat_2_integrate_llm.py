# In this code example you'll understand how every node is getting appended to next via graph  
# and this is appeding becoz if you see MessagesState, It's has add_message function
import os
from typing import Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
# Initialize LLM
# Instead of ChatGoogleGenerativeAI you can use init_chat_model()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
# model = init_chat_model("google_genai:gemini-2.5-flash-lite") #https://docs.langchain.com/oss/python/langchain/models#basic-usage

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    print("\n\n I'm in chatbot. state =>", state)
    
    # Call LLM with the messages
    response = llm.invoke(state["messages"])
    
    print(f"\nLLM-Response->", response)
    return {"messages": [response]}

def sample_node(state: State):
    print("\n\n I'm in sample_node. state =>", state)
    return {"messages": ["3. Sample Message Appended"]}

graph = StateGraph(State)

graph.add_node("chatbot", chatbot) 
graph.add_node("sample_node", sample_node)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", "sample_node")
graph.add_edge("sample_node", END)

compiled_graph = graph.compile()

try:
    updated_state = compiled_graph.invoke({"messages": ["1.Hey!, My name is pushpak"]})
    print('\n\nupdated_state->', updated_state)
except Exception as e:
    if "429" in str(e):
        print("\n❌ Rate limit exceeded! Wait 30 seconds and retry.")
    else:
        print(f"\n❌ Error: {e}")