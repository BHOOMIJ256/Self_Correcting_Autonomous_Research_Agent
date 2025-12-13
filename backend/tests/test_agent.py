import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from src.agents.workflow import create_graph
from src.utils.judge import GroqJudge

# Initialize our Free Judge
groq_judge = GroqJudge()

def test_research_agent_relevancy():
    print("\n🚀 Starting Agent Evaluation...")
    
    # 1. Define the input
    topic = "What is the capital of France?"
    
    # 2. Run your actual Agent Application
    app = create_graph()
    result = app.invoke({"topic": topic})
    actual_output = result['final_summary']
    retrieved_context = result['search_results'] # We need this to check hallucinations
    
    print(f"🤖 Agent Answer: {actual_output}")

    # 3. Define the Metric: "Is the answer relevant to the question?"
    # We pass our custom groq_judge so it doesn't ask for OpenAI key
    relevancy_metric = AnswerRelevancyMetric(
        threshold=0.5, 
        model=groq_judge, 
        include_reason=True
    )

    # 4. Define the Test Case
    test_case = LLMTestCase(
        input=topic,
        actual_output=actual_output,
        retrieval_context=retrieved_context 
    )

    # 5. Run the Test
    assert_test(test_case, [relevancy_metric])