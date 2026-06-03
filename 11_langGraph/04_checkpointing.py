# https://docs.langchain.com/oss/python/langgraph/persistence#checkpoints
# No rocket science in this, just compile graph with db 
# make sure u run mongo docker container
## Checkpointing specically helping you to create personal chatbot, where it'll reatin your data.
import os
from typing import Annotated, Literal, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph, add_messages
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver  

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
def chatbot(state: State):
    response = llm.invoke(state.get("messages"))    
    return {"messages":[response]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# we shifted these 2 steps below
# graph = graph_builder.compile()
# updated_state = graph.invoke(State({"messages": ["What is my name ?"]}))

# ============= check pointer code ====================
# https://docs.langchain.com/oss/python/langgraph/add-memory#use-in-production
MONGODB_URI = "mongodb://admin:admin@localhost:27017/pushpak-checkpointDB?authSource=admin"  # authSource=admin is required for root user
with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    
    checkpointed_graph = graph_builder.compile(checkpointer=checkpointer)  #1.Important compile step
    config = {
        "configurable": {
            "thread_id": "2" #This must be unique, it helps to retrieve specific chat. 
        }
    }
    
    for chunk in checkpointed_graph.stream(   # instead of invoke im using stream for readable response 
        State({"messages": ["Hey! I'm learning AI/ML  "]}), #first give ur personal data to it from here and then ask questions accordingly
        config, #2 pass config in invoke
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
        
        
    