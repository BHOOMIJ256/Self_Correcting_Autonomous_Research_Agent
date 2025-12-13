from langchain_groq import ChatGroq
import os

def get_llm(temperature=0):
    """Returns the Groq LLM instance"""
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=temperature,
        max_retries=2
        # api_key is read automatically from environment
    )