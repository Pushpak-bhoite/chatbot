# In this code example you'll understand how every node is getting appended to next via graph  
# and this is appeding becoz if you see MessagesState, It's has add_message function
from langgraph.graph import StateGraph, MessagesState, START, END

def chatbot(state:MessagesState):
    print("\n\n I'm in chatbot. state =>", state)
    return {"messages":["2. This message is from chatbot"]}

def sample_node(state: MessagesState):
    print("\n\n I'm in sample_node. state =>", state)
    return {"messages": ["3. Sample Message Appended"]}

graph = StateGraph(MessagesState)

graph.add_node("chatbot", chatbot) # THis is kind of we are registering the node to graph 
graph.add_node("sample_node", sample_node)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", "sample_node")
graph.add_edge("sample_node", END)

compiled_graph = graph.compile()
updated_state = compiled_graph.invoke({"messages": ["1.Hey!, My name this is pushpak"]})

print('\n\nupdated_state->', updated_state)