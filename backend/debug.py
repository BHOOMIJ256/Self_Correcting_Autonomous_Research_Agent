import os
import sys

print(f"Current Working Directory: {os.getcwd()}")
print(f"Script Location: {os.path.dirname(os.path.abspath(__file__))}")

print("\n--- Scanning for src/graph/workflow.py ---")
target_path = os.path.join(os.getcwd(), "src", "graph", "workflow.py")
if os.path.exists(target_path):
    print(f"✅ FOUND IT: {target_path}")
else:
    print(f"❌ NOT FOUND: {target_path}")

print("\n--- Full File Tree under 'backend' ---")
start_dir = "."
for root, dirs, files in os.walk(start_dir):
    # Skip __pycache__ and venv to keep output clean
    if "__pycache__" in root or "venv" in root:
        continue
    
    level = root.replace(start_dir, '').count(os.sep)
    indent = ' ' * 4 * (level)
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")