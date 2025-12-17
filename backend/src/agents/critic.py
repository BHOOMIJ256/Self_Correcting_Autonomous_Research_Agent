from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm

def critic_node(state: AgentState):
    print("--- [Critic Agent] Reviewing research quality ---")
    
    notes = state['research_notes']
    topic = state['topic']
    current_loop = state.get('loop_count', 0)
    llm = get_llm()
    
    # 1. Safety Check: Force approval if we loop too much
    if current_loop >= 3:
        print("⚠️ Loop limit reached. Forcing approval.")
        return {"critique": "approve"}

    # 2. Strict Grading Prompt
    system_prompt = """You are a Research Supervisor.
    Review the provided research notes on '{topic}'.
    
    Your Logic:
    1. Does the research cover the basics?
    2. Does it include pros/cons or challenges?
    3. Is it deep enough for a technical report?
    
    Output Instructions:
    - If GOOD: Output exactly "approve".
    - If BAD: Output a SINGLE search query to find the missing info. 
      - Do NOT output reasoning. 
      - Do NOT output "The research is missing X".
      - JUST the query.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", f"Current Notes:\n{notes}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    decision = result.content.strip()
    
    # 3. Handle Decision
    if "approve" in decision.lower():
        print("✅ Critic Approved.")
        return {"critique": "approve"}
    else:
        # Clean up the query just in case the LLM adds quotes
        new_query = decision.replace('"', '').replace("Search query:", "").strip()
        
        print(f"❌ Critic Rejected. Feedback Loop #{current_loop+1}")
        print(f"🔍 New Search Query: {new_query}")
        
        return {
            "critique": "reject", 
            "plan": [new_query], # Overwrite the plan with the new targeted query
            "loop_count": current_loop + 1
        }