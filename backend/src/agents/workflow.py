from langgraph.graph import StateGraph, END
from src.graph.state import AgentState

# Imports
from src.agents.researcher import search_node
from src.agents.reader import read_node
from src.agents.writer import write_node
from src.agents.planner import plan_node
from src.agents.critic import critic_node

# --- The Router Function ---
def decide_next_step(state: AgentState):
    """
    Determines if we go to 'write' or back to 'search'
    based on the critic's output.
    """
    critique = state.get("critique", "approve")
    
    if "approve" in critique:
        return "write"
    else:
        return "search"

def create_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("planner", plan_node)
    workflow.add_node("search", search_node)
    workflow.add_node("read", read_node)
    workflow.add_node("critic", critic_node) # <--- NEW
    workflow.add_node("write", write_node)

    # 2. Define Edges
    workflow.set_entry_point("planner")
    
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "read")
    workflow.add_edge("read", "critic") # Read now goes to Critic, not Write
    
    # 3. Conditional Logic
    workflow.add_conditional_edges(
        "critic",          # From the Critic node...
        decide_next_step,  # ...run this function...
        {                  # ...and map the result to a node.
            "write": "write",
            "search": "search"
        }
    )
    
    workflow.add_edge("write", END)

    return workflow.compile()