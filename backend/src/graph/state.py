# src/graph/state.py
from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str                # The input topic (e.g., "AI in Healthcare")
    search_results: List[str] # Raw results from the Search Agent
    research_notes: str       # Filtered notes from the Read Agent
    final_summary: str        # Output from the Write Agent