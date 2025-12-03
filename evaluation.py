"""
Evaluation system for testing agent responses
"""
from google import genai
import os

# Use consistent model name
MODEL_NAME = "gemini-2.0-flash-exp"  # Or "gemini-2.5-flash" if available

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

TEST_SET = [
    ("What is Python?", "programming"),
    ("What is AI?", "intelligence"),
    ("Define machine learning", "learning"),
]

def run_evaluation():
    """
    Run evaluation tests on the AI agent
    """
    results = []
    score = 0

    for q, keyword in TEST_SET:
        try:
            res = client.models.generate_content(
                model=MODEL_NAME,
                contents=q
            )

            response_text = res.text if hasattr(res, 'text') else str(res)
            ok = keyword.lower() in response_text.lower()

            if ok:
                score += 1

            results.append({
                "question": q,
                "passed": ok,
                "response": response_text[:140]
            })
        
        except Exception as e:
            results.append({
                "question": q,
                "passed": False,
                "response": f"Error: {str(e)}"
            })

    accuracy = (score / len(TEST_SET) * 100) if TEST_SET else 0

    return {
        "accuracy": accuracy,
        "results": results
    }