import sys
import os
from dotenv import load_dotenv # Import this first!

# 1. Load the environment variables BEFORE importing anything else
# We point it explicitly to the .env file in the root folder (one level up)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) # Go up to sentinel_research_agent/
dotenv_path = os.path.join(root_dir, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✅ Loaded .env from: {dotenv_path}")
else:
    print("❌ ERROR: .env file not found at:", dotenv_path)

# 2. Add backend to path (The fix we did earlier)
sys.path.append(current_dir)

# 3. NOW import your app code
# If we imported this at the top, it would crash because keys weren't loaded yet
from src.agents.workflow import create_graph

def main():
    print("Initializing Sentinel Phase 1...")
    
    # Create the graph
    app = create_graph()
    
    # Define the input
    topic = input("Enter a research topic: ")
    initial_state = {"topic": topic}
    
    # Run the graph
    try:
        result = app.invoke(initial_state)
        print("\n" + "="*50)
        print("FINAL SUMMARY")
        print("="*50 + "\n")
        print(result['final_summary'])
    except Exception as e:
        print(f"\n❌ Runtime Error: {e}")

if __name__ == "__main__":
    main()