"""
Context engineering for conversation summarization
"""
from google import genai
import os

# Use consistent model name
MODEL_NAME = "gemini-2.5-flash"  # Or "gemini-2.5-flash" if available

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def summarize_history(messages):
    """
    Summarize conversation history for context
    """
    if not messages:
        return "No previous conversation history."

    text_block = ""
    for m in messages:
        query = m.get('query', '')
        response = m.get('response', '')
        text_block += f"User: {query}\nAssistant: {response}\n\n"

    # Limit history length to avoid token issues
    if len(text_block) > 2000:
        text_block = text_block[-2000:]

    prompt = f"""
Summarize the following conversation history into important facts,
preferences, or unresolved questions to help an assistant continue:

{text_block}

Provide a short bullet-point summary:
"""

    try:
        res = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        summary = res.text if hasattr(res, 'text') else str(res)
        return summary.strip()
    
    except Exception as e:
        print(f"Error summarizing history: {e}")
        return "Unable to summarize conversation history."