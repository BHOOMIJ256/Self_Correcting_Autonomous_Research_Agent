import warnings
# Silence the annoying deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# We use the community version because it is stable
from langchain_community.tools.tavily_search import TavilySearchResults
from src.graph.state import AgentState

# Since conftest.py loads the API key now, this line will NOT crash anymore!
tavily_tool = TavilySearchResults(max_results=3)

def search_node(state: AgentState):
    print(f"--- [Search Agent] Searching for: {state['topic']} ---")
    
    try:
        search_result = tavily_tool.invoke(state['topic'])
    except Exception as e:
        return {"search_results": [f"Error searching: {str(e)}"]}
    
    # Handle list vs string return types
    if isinstance(search_result, list):
        docs = [res.get('content', '') for res in search_result]
    else:
        docs = [str(search_result)]
    
    return {"search_results": docs}