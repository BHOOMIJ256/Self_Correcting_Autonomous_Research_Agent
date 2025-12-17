import sys
import os
from dotenv import load_dotenv # 1. Import this first

# 2. Force load the .env file immediately
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) # Go up to sentinel_research_agent/
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)

# 3. Fix the path so Python finds 'src'
sys.path.append(current_dir)

# 4. NOW import the agents (Safe because keys are loaded)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.workflow import create_graph

app = FastAPI(title="Sentinel Research Agent API")

# Define the Request Body
class ResearchRequest(BaseModel):
    topic: str
    search_mode: str = "Auto"   # <--- NEW
    model_type: str = "Llama-3.3" # <--- NEW

@app.post("/research")
def run_research(request: ResearchRequest):
    try:
        # Pass inputs to State
        initial_state = {
            "topic": request.topic, 
            "search_mode": request.search_mode, 
            "model_name": request.model_type
        }
        workflow = create_graph()
        result = workflow.invoke(initial_state)
        
        return {
            "topic": request.topic,
            "final_summary": result.get("final_summary", "Error"),
            "sources": result.get("search_results", []),
            "plan": result.get("plan", []),
            "loop_count": result.get("loop_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)