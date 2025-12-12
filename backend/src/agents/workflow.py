# src/graph/workflow.py
from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.agents.nodes import search_node, read_node, write_node

def create_graph():
    # 1. Initialize the graph with our state
    workflow = StateGraph(AgentState)

    # 2. Add the nodes (the agents)
    workflow.add_node("search", search_node)
    workflow.add_node("read", read_node)
    workflow.add_node("write", write_node)

    # 3. Define the edges (the flow)
    # Entry Point -> Search
    workflow.set_entry_point("search")
    
    # Search -> Read
    workflow.add_edge("search", "read")
    
    # Read -> Write
    workflow.add_edge("read", "write")
    
    # Write -> End
    workflow.add_edge("write", END)

    # 4. Compile the graph
    app = workflow.compile()
    return app