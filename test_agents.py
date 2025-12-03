"""
Test script to debug the agents system
Run this with: python test_agents.py
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("JARVIS AGENT DEBUG TEST")
print("="*60)

# Check environment variables
print("\n1. Checking Environment Variables:")
print("-" * 60)
google_key = os.getenv("GOOGLE_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(f"GOOGLE_API_KEY: {'✓ Set' if google_key else '✗ NOT SET'}")
if google_key:
    print(f"  Length: {len(google_key)} chars")
print(f"SUPABASE_URL: {'✓ Set' if supabase_url else '✗ NOT SET'}")
print(f"SUPABASE_KEY: {'✓ Set' if supabase_key else '✗ NOT SET'}")

if not google_key:
    print("\n⚠️  ERROR: GOOGLE_API_KEY is required!")
    print("Please add it to your .env file:")
    print("GOOGLE_API_KEY=your_api_key_here")
    exit(1)

# Test imports
print("\n2. Testing Imports:")
print("-" * 60)

try:
    from google import genai
    print("✓ google-genai imported successfully")
except ImportError as e:
    print(f"✗ Failed to import google-genai: {e}")
    print("Run: pip install google-genai")
    exit(1)

try:
    import database
    print("✓ database module imported")
    print(f"  DB Status: {'Connected' if database.db else 'Not connected'}")
except ImportError as e:
    print(f"✗ Failed to import database: {e}")
    exit(1)

try:
    import memory
    print("✓ memory module imported")
except ImportError as e:
    print(f"✗ Failed to import memory: {e}")
    exit(1)

try:
    import observability
    print("✓ observability module imported")
except ImportError as e:
    print(f"✗ Failed to import observability: {e}")
    exit(1)

try:
    import context_engineering
    print("✓ context_engineering module imported")
except ImportError as e:
    print(f"✗ Failed to import context_engineering: {e}")
    exit(1)

try:
    import agents
    print("✓ agents module imported")
except ImportError as e:
    print(f"✗ Failed to import agents: {e}")
    exit(1)

# Test Gemini API
print("\n3. Testing Gemini API:")
print("-" * 60)

try:
    client = genai.Client(api_key=google_key)
    print("✓ Gemini client created")
    
    # Test a simple API call
    print("  Testing API call with simple prompt...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say 'Hello' in one word"
    )
    
    print(f"✓ API call successful")
    print(f"  Response type: {type(response)}")
    
    if hasattr(response, 'text'):
        print(f"  Response text: {response.text[:100]}")
    else:
        print(f"  Response (no .text attribute): {str(response)[:100]}")
    
except Exception as e:
    print(f"✗ Gemini API test failed: {e}")
    import traceback
    print(traceback.format_exc())

# Test Agent System
print("\n4. Testing Agent System:")
print("-" * 60)

async def test_agents():
    try:
        print("Testing with query: 'what is python'")
        exec_result, ai_response = await agents.parallel_run("what is python")
        
        print(f"\nExecutor Result: {exec_result}")
        print(f"\nAI Response: {ai_response}")
        
        if ai_response and "error" not in ai_response.lower():
            print("\n✓ Agent system working correctly!")
        else:
            print("\n⚠️  Agent system returned an error response")
        
    except Exception as e:
        print(f"\n✗ Agent test failed: {e}")
        import traceback
        print(traceback.format_exc())

print("\nRunning async agent test...")
asyncio.run(test_agents())

print("\n" + "="*60)
print("DEBUG TEST COMPLETE")
print("="*60)