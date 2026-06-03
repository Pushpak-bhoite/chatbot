# we have best ex for this topic - https://docs.langchain.com/oss/python/langgraph/workflows-agents#prompt-chaining
from typing import Literal, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]
    

def chatbot(state: State):
    response = llm.invoke(state['user_query'])
    print('\n\nchatbot_response->', response.content)
    return {"llm_output": response.content}  # Return only what changed

def evaluate_response(state: State) -> Literal["strong_chatbot", "end_node"]:
    if True:
        return "end_node"
    
    return "strong_chatbot"

def strong_chatbot(state: State):
    response = llm.invoke(state['user_query'])
    print('\n\nstrong_bot->', response.content)
    return {"llm_output": response.content}  # Return only what changed

def end_node(state: State):
    return {}  # Nothing to update

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("strong_chatbot", strong_chatbot)
graph_builder.add_node("end_node", end_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("strong_chatbot", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "hey! what is 2 + 2 "}))
print("\n\nupdated_state->", graph_builder)
