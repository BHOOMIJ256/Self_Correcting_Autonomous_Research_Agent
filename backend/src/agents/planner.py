from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm

def plan_node(state: AgentState):
    print(f"--- [Planner Agent] Breaking down topic: {state['topic']} ---")
    
    topic = state['topic']
    # Use a slightly higher temperature to prevent repetition loops
    llm = get_llm(temperature=0.2) 
    
    system_prompt = """You are a Research Planner.
    Your task: Break down the given topic into exactly 3 short, specific search queries.
    
    Rules:
    1. Output ONLY the 3 queries.
    2. Separate them by newlines.
    3. Do not number them (no 1., 2., etc).
    4. Do not add intro or outro text.
    5. Keep queries under 10 words each.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", f"Topic: {topic}")
    ])
    
    try:
        result = chain = prompt | llm
        response = chain.invoke({"topic": topic})
        raw_content = response.content
        
        # --- SAFETY CHECK ---
        # If Groq returns the "PUSHDATA" glitch or empty text, fail gracefully
        if "PUSHDATA" in raw_content or len(raw_content) < 5:
            print(f"⚠️ Planner Glitch Detected. Falling back to original topic.")
            return {"plan": [topic]}

        # Split and clean
        plan = raw_content.strip().split('\n')
        plan = [p.strip() for p in plan if p.strip()]
        
        # Ensure we don't have empty lists
        if not plan:
            plan = [topic]
            
        print(f"📋 Generated Plan: {plan}")
        return {"plan": plan}
        
    except Exception as e:
        print(f"⚠️ Planner Error: {e}. Falling back to topic.")
        return {"plan": [topic]}