"""
Database configuration - Central database connection
This file should be imported by all other modules that need DB access
"""
import os
from dotenv import load_dotenv

try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Warning: Supabase not available. Memory features will be limited.")

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Initialize database connection
db = None
if SUPABASE_AVAILABLE and url and key:
    try:
        db = create_client(url, key)
        print("✓ Supabase connected successfully")
    except Exception as e:
        print(f"✗ Supabase connection error: {e}")
        db = None
else:
    if not url or not key:
        print("ℹ️  Supabase credentials not found - running without database")