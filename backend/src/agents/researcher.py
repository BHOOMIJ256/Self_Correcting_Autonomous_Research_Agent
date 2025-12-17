import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.tools.tavily_search import TavilySearchResults
from src.tools.arxiv import arxiv_search_tool  # <--- Import your new tool
from src.graph.state import AgentState
from src.utils.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

# Initialize tools
tavily = TavilySearchResults(max_results=2)
# We list available tools for the LLM to choose
tools_map = {
    "web": tavily,
    "academic": arxiv_search_tool
}

# ... keep your imports ...

def search_node(state: AgentState):
    queries = state.get('plan', [state['topic']])
    search_mode = state.get('search_mode', 'auto').lower() # <--- GET USER CHOICE
    all_results = []
    llm = get_llm()
    
    for query in queries:
        # DEFAULT: Auto-Routing
        tool_name = "Tavily" 
        tool_to_use = tavily
        
        # LOGIC: Override based on user choice
        if "deep" in search_mode or "academic" in search_mode:
            print(f"--- [Search Agent] Forced Mode: Academic (ArXiv) ---")
            tool_name = "ArXiv"
            tool_to_use = arxiv_search_tool
        elif "fast" in search_mode or "web" in search_mode:
            print(f"--- [Search Agent] Forced Mode: Web (Tavily) ---")
            tool_name = "Tavily"
            tool_to_use = tavily
        else:
            # ORIGINAL AUTO LOGIC
            router_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a Tool Router. Output 'academic' if the query is scientific. Output 'web' for news. Output ONLY the word."),
                ("user", query)
            ])
            decision = (router_prompt | llm).invoke({}).content.strip().lower()
            if "academic" in decision:
                tool_name = "ArXiv"
                tool_to_use = arxiv_search_tool
        
        # Execute
        print(f"--- [Search Agent] Using {tool_name} for: {query} ---")
        try:
            if tool_name == "Tavily":
                res = tool_to_use.invoke(query)
                content = [f"Web Source: {r['content']}" for r in res] if isinstance(res, list) else [str(res)]
            else:
                res = tool_to_use.invoke(query)
                content = [f"Academic Paper: {res}"]
            all_results.extend(content)
        except Exception as e:
            print(f"⚠️ Error with {tool_name}: {e}")
            
    return {"search_results": all_results}