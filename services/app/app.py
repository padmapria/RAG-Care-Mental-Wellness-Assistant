from flask import Flask, request, jsonify, session
import time
import uuid
import logging
from rag_assistant import extract_llm_response_relevance_score
from db import save_question, save_feedback, get_recent_questions  # Import functions for database interactions

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RAG_Mental_Wellness_Assistant")  # Custom logger name for the Flask app

# Endpoint to return a greeting message
@app.route('/hello', methods=['GET'])
def say_hello():
    """
    Simple endpoint to return a greeting message.
    """
    logger.info("Received request for /hello endpoint")
    return jsonify({"message": "Hello!"}), 200
    
# Endpoint to handle incoming questions
@app.route('/ask', methods=['POST'])
def handle_question():
    """
    API endpoint to receive a question from the user, process it, and return an answer.
    - Expects a JSON payload with the key 'question'.
    - Calls the assistant to get the answer.
    - Saves the question and answer into the database.
    """
    try:
        request_data = request.get_json()
        user_question = request_data.get('question')
        
        # Check if question is provided in the request
        if not user_question:
            logger.warning("Received a request without a question")
            return jsonify({"error": "Please provide a valid question"}), 400
        
        # Generate a unique identifier for the question
        question_uuid = str(uuid.uuid4())
        logger.info(f"Generated new UUID '{question_uuid}' for the question: '{user_question}'")

        # Simulate assistant processing to get an answer
        logger.info(f"Processing the question: '{user_question}'")
        start_time = time.time()
        
        # Function that retrieves response from openai llm
        llm_response,relevance,relevance_expl = extract_llm_response_relevance_score(user_question)  
        processing_time = time.time() - start_time

        logger.info(f"Assistant response generated in {processing_time:.2f} seconds for question UUID '{question_uuid}'")
        
        model_used = "openai_4o"
        # Save question and assistant response in the database
        logger.info(f"Saving the conversation (Question ID: {question_uuid}) to the database")
        save_question(question_uuid, user_question, llm_response, model_used,processing_time, 
        relevance, relevance_expl)
        
        logger.info(f"Question and response saved successfully for UUID: {question_uuid}")

        # Return the answer in the response
        return jsonify({
            "question_uuid": question_uuid,
            "question": user_question,
            "answer": llm_response,
            "relevance" : relevance, 
            "relevance_explanation": relevance_expl,
            "response_generated_by": model_used,
            "evaluation_by" : "openai_3.5"
        }), 200

    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error occurred"}), 500


# Endpoint to handle feedback submission
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    API endpoint to receive feedback for a question.
    - Expects a JSON payload with 'question_id' and 'feedback' (1 for like, -1 for dislike).
    - Saves feedback to the database.
    """
    try:
        feedback_data = request.get_json()
        question_id = feedback_data.get('question_uuid')
        user_feedback = feedback_data.get('feedback')

        if not question_id or user_feedback not in [-1, 1]:
            logger.warning(f"Invalid feedback data received. Data: {feedback_data}")
            return jsonify({"error": "Invalid feedback or question ID"}), 400

        # Save feedback in the database
        logger.info(f"Saving feedback for Question ID: {question_id}")
        save_feedback(question_id, user_feedback)
        logger.info(f"Feedback for Question ID: {question_id} saved successfully")

        return jsonify({"message": "Feedback submitted successfully"}), 200

    except Exception as e:
        logger.error(f"Error occurred while submitting feedback: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error occurred"}), 500


# Endpoint to retrieve recent questions with optional rating filter
@app.route('/recent_questions', methods=['GET'])
def get_recent_questions_list():
    """
    API endpoint to retrieve recent questions.
    - Optional query parameter 'rating' to filter by rating.
    """
    try:
        recent_questions = get_recent_questions(limit=5)
        logger.info(f"Retrieved {len(recent_questions)} recent questions from the database")

        return jsonify(recent_questions), 200

    except Exception as e:
        logger.error(f"Error occurred while retrieving recent questions: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error occurred"}), 500

# Main entry point to run the Flask app
if __name__ == '__main__':
    # Bind to 0.0.0.0 and specify port
    app.run(debug=True, host='0.0.0.0', port=5000)
