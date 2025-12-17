from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str
    plan: List[str]
    search_results: List[str]
    research_notes: str
    final_summary: str
    critique: str
    loop_count: int
    # --- NEW FIELDS ---
    search_mode: str  # "auto", "academic", "web"
    model_name: str   # "llama-3.3", "gpt-4o"