# backend/src/utils/judge.py
from deepeval.models import DeepEvalBaseLLM
from langchain_groq import ChatGroq

class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="llama-3.3-70b-versatile"): # Use 70b for better judging logic
        self.model_name = model_name
        self.groq = ChatGroq(model=model_name, temperature=0)

    def load_model(self):
        return self.groq

    def generate(self, prompt: str) -> str:
        res = self.groq.invoke(prompt)
        return res.content

    async def a_generate(self, prompt: str) -> str:
        res = await self.groq.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return self.model_name