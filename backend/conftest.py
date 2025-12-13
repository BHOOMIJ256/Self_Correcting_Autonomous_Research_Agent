import sys
import os
from dotenv import load_dotenv

# --- 1. FORCE LOAD .ENV FIRST ---
# Get the path to the 'backend' folder
backend_path = os.path.dirname(os.path.abspath(__file__))
# Go up one level to find the 'sentinel_research_agent' root
root_path = os.path.dirname(backend_path)
dotenv_path = os.path.join(root_path, '.env')

# Load it immediately
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✅ [conftest] Loaded environment variables from: {dotenv_path}")
else:
    print(f"❌ [conftest] CRITICAL: .env file not found at {dotenv_path}")

# --- 2. FIX PYTHON PATH ---
# Add backend to the path so 'src' imports work
if backend_path not in sys.path:
    sys.path.append(backend_path)