import os
import sys

# Add the project root and app directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app_directory = os.path.join(project_root, 'app')
sys.path.append(app_directory)

try:
    from flask_app import app  # Import from the app directory now
    from db import save_question, save_feedback, get_recent_questions
    from rag_assistant import extract_llm_response_relevance_score  # Import your module
    print("Imports successful!")
except Exception as e:
    print(f"Error importing modules: {e}")
