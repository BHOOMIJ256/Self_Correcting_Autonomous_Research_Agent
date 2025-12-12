# src/agents/nodes.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from src.graph.state import AgentState
import os

# --- Setup ---
# Make sure you have TAVILY_API_KEY and OPENAI_API_KEY in your .env
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tavily_tool = TavilySearchResults(max_results=3)

# --- Node 1: Search Agent ---
def search_node(state: AgentState):
    print(f"--- [Search Agent] Searching for: {state['topic']} ---")
    
    # Run the search
    search_result = tavily_tool.invoke(state['topic'])
    
    # Format results slightly
    docs = [res['content'] for res in search_result]
    
    return {"search_results": docs}

# --- Node 2: Read Agent ---
def read_node(state: AgentState):
    print("--- [Read Agent] Reading and extracting key facts ---")
    
    docs = state['search_results']
    topic = state['topic']
    
    # Prompt the LLM to act as a note-taker
    system_prompt = """You are a senior researcher. 
    Read the following search snippets and extract the 3-5 most important facts 
    relevant to the topic '{topic}'. Ignore irrelevant details."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Snippets:\n\n" + "\n---\n".join(docs))
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    
    return {"research_notes": result.content}

# --- Node 3: Write Agent ---
def write_node(state: AgentState):
    print("--- [Write Agent] Synthesizing final summary ---")
    
    notes = state['research_notes']
    topic = state['topic']
    
    system_prompt = """You are a technical writer. 
    Write a concise, professional summary on '{topic}' using the provided research notes.
    Cite the facts implicitly."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Research Notes:\n" + notes)
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    
    return {"final_summary": result.content}