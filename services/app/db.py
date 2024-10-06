#app/db.py
import os
import mysql.connector
from mysql.connector import pooling
from datetime import datetime  # Import datetime for timestamp handling
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.dbdetails")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("db")  # Custom logger name for the Flask app

# Function to get a SQL connection
def get_mysql_connection():
    config = {
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'root_pass'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '3308'),
        'database': os.getenv('DB_NAME', 'rag_db')
    }
    connection = mysql.connector.connect(**config)
    return connection

def save_question(question_id, question,user_question,
            question_length_diff, answer_data, model_used, timetaken, 
relevance, relevance_expl, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()  # Get current time if none provided

    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()  # Get the connection
        cursor = conn.cursor()          # Initialize the cursor

        # Prepare the data
        data_to_insert = (
            question_id,
            question,
            user_question,
            question_length_diff,
            answer_data,
            model_used,
            timetaken,
            relevance,
            relevance_expl,
            timestamp,
        )

        # Print the data that will be sent to the database        
        logger.info(f"Data being sent to the database: '{data_to_insert}'")

        cursor.execute(
            """
            INSERT INTO requests
            (id, question, user_question,question_length_diff, answer, model_used, 
            response_time_in_seconds, relevance, relevance_expl, `timestamp`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP));
            """,
            data_to_insert
        )
        
        conn.commit()  # Commit the transaction to save changes

    except Exception as e:
        print(f"Error saving question: {e}")  # Log the error or handle it as needed
    finally:
        if cursor is not None:
            cursor.close()  # Close cursor only if it was created
        if conn is not None:
            conn.close()    # Close connection only if it was created
            
            

def save_feedback(question_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()  # Get current time if none provided

    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (question_id, feedback, created_at) VALUES (%s, %s, COALESCE(%s, CURRENT_TIMESTAMP))",
            (question_id, feedback, timestamp),
        )
        conn.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error saving feedback: {e}")  # Log the error or handle it as needed
    finally:
        if cursor is not None:
            cursor.close()  # Close cursor only if it was created
        if conn is not None:
            conn.close()    # Close connection only if it was created

def get_recent_questions(limit=5):
    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Modify query to fetch limited recent questions
        cursor.execute(f"SELECT * FROM requests LIMIT {limit}")
        result = cursor.fetchall()

        # Get column names
        column_names = [i[0] for i in cursor.description]

        # Convert results to list of dictionaries
        recent_questions = [dict(zip(column_names, row)) for row in result]

        return recent_questions  # Return the fetched results with column names
    except Exception as e:
        print(f"Error retrieving recent questions: {e}")  # Log the error or handle it as needed
        return []  # Return an empty list on error
    finally:
        if cursor is not None:
            cursor.close()  # Close cursor only if it was created
        if conn is not None:
            conn.close()    # Close connection only if it was created
