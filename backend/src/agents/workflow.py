from langgraph.graph import StateGraph, END
from src.graph.state import AgentState

# Now we import from the package, not the 'nodes' file
from src.agents.researcher import search_node
from src.agents.reader import read_node
from src.agents.writer import write_node
def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("search", search_node)
    workflow.add_node("read", read_node)
    workflow.add_node("write", write_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "read")
    workflow.add_edge("read", "write")
    workflow.add_edge("write", END)

    return workflow.compile()