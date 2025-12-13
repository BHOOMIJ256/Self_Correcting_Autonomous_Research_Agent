from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm

def read_node(state: AgentState):
    print("--- [Read Agent] Reading and extracting key facts ---")
    
    docs = state['search_results']
    topic = state['topic']
    llm = get_llm()
    
    system_prompt = """You are a senior researcher. 
    Read the search snippets below and extract the 3-5 most important facts 
    relevant to the topic '{topic}'. 
    If the snippets are empty or irrelevant, say 'No relevant information found.'"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Snippets:\n\n" + "\n---\n".join(docs))
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    
    return {"research_notes": result.content}