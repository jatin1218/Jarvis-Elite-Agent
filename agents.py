"""
Multi-agent system with Planner, Executor, and Conversation agents
"""
import asyncio
import os
from google import genai

from memory import MemoryAgent
from observability import obs
from context_engineering import summarize_history

# Use consistent model name
MODEL_NAME = "gemini-2.5-flash"  # Or "gemini-2.5-flash" if available

# Initialize client with better error handling
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment variables!")
        print("Please add GOOGLE_API_KEY to your .env file")
    client = genai.Client(api_key=api_key)
    print("✓ Gemini API client initialized")
except Exception as e:
    print(f"✗ Failed to initialize Gemini client: {e}")
    client = None

memory = MemoryAgent()

# ---------- PLANNER ----------
class PlannerAgent:
    def classify(self, text):
        try:
            obs.log("Planner", "classify", text)
            if any(w in text.lower() for w in ["open", "search", "scroll", "play"]):
                return "EXECUTOR"
            return "AI"
        except Exception as e:
            print(f"Error in Planner.classify: {e}")
            return "AI"

# ---------- EXECUTOR ----------
class ExecutorAgent:
    async def execute_async(self, command):
        try:
            obs.log("Executor", "execute_async", command)
            obs.metric("tool_call")
            await asyncio.sleep(0.2)   # simulate parallel call
            return f"[SYSTEM] Executed: {command}"
        except Exception as e:
            print(f"Error in Executor.execute_async: {e}")
            return f"[SYSTEM ERROR] Failed to execute: {command}"

# ---------- CONVERSATION ----------
class ConversationAgent:
    async def ask_async(self, prompt):
        """
        Process conversation with Gemini API
        """
        try:
            obs.log("Gemini", "ask_async", prompt[:100])
            obs.metric("ai_call")
        except Exception as e:
            print(f"Warning: Observability logging failed: {e}")

        # Check if client is initialized
        if not client:
            error_msg = "Gemini API client not initialized. Check your GOOGLE_API_KEY."
            print(f"[ERROR] {error_msg}")
            return error_msg

        try:
            # Get conversation history
            history = memory.recent()
            
            # Summarize history
            summary = summarize_history(history)

            final_prompt = f"""
Conversation Summary:
{summary}

User Question:
{prompt}
"""

            # Call Gemini API
            res = client.models.generate_content(
                model=MODEL_NAME,
                contents=final_prompt
            )

            # Extract response text
            if hasattr(res, 'text'):
                response = res.text
            else:
                response = str(res)

            # Save to memory
            memory.save(prompt, response)

            return response
        
        except AttributeError as e:
            error_msg = f"API Response Error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            obs.log("Gemini", "error", error_msg)
            return "I received a response but couldn't read it. Please try again."
        
        except Exception as e:
            error_msg = f"Error in AI agent: {str(e)}"
            print(f"[ERROR] {error_msg}")
            obs.log("Gemini", "error", error_msg)
            return f"I apologize, but I encountered an error: {str(e)}"


planner = PlannerAgent()
executor = ExecutorAgent()
ai_agent = ConversationAgent()


async def parallel_run(command):
    """
    Execute Executor + AI simultaneously if appropriate
    """
    try:
        decision = planner.classify(command)

        if decision == "EXECUTOR":
            exec_task = asyncio.create_task(
                executor.execute_async(command)
            )
            ai_task = asyncio.create_task(
                ai_agent.ask_async(
                    f"Acknowledge the system task: {command}"
                )
            )
            exec_result = await exec_task
            ai_msg = await ai_task
            return exec_result, ai_msg
        else:
            ai_msg = await ai_agent.ask_async(command)
            return None, ai_msg
    
    except Exception as e:
        error_msg = f"Error in parallel_run: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return None, f"System error: {str(e)}"