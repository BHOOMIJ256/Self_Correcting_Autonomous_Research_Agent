# main.py
from dotenv import load_dotenv
from src.graph.workflow import create_graph

# Load environment variables (API Keys)
load_dotenv()

def main():
    print("Initializing Sentinel Phase 1...")
    
    # Create the graph
    app = create_graph()
    
    # Define the input
    topic = input("Enter a research topic: ")
    initial_state = {"topic": topic}
    
    # Run the graph
    # We use .invoke() to run it synchronously
    result = app.invoke(initial_state)
    
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50 + "\n")
    print(result['final_summary'])

if __name__ == "__main__":
    main()