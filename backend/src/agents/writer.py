from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm

def write_node(state: AgentState):
    print("--- [Write Agent] Synthesizing final summary ---")
    
    notes = state['research_notes']
    topic = state['topic']
    llm = get_llm()
    
    system_prompt = """You are a technical writer. 
    Write a concise, professional summary on '{topic}' using the provided research notes.
    Do not hallucinate facts not present in the notes."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Research Notes:\n" + notes)
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    
    return {"final_summary": result.content}