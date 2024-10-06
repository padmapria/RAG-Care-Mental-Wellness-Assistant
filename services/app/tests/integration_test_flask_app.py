# tests/integration_test_flask_app.py
import os
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app_directory = os.path.join(project_root, 'app')
sys.path.append(app_directory)


import unittest
from unittest.mock import patch, MagicMock
from flask import json
from flask_app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # Mocking /hello endpoint
    def test_hello_endpoint(self):
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Hello!')

    # Mocking /ask endpoint
    @patch('flask_app.extract_llm_response_relevance_score')
    def test_ask_endpoint_success(self, mock_extract_llm_response_relevance_score):
        mock_extract_llm_response_relevance_score.return_value = ('rewritten_question', 'llm_response', 'relevance', 'relevance_expl')
        response = self.app.post('/ask', json={'question': 'What is the meaning of life?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('question_uuid', response.json)
        self.assertIn('question', response.json)
        self.assertIn('user_question', response.json)
        self.assertIn('answer', response.json)
        self.assertIn('relevance', response.json)
        self.assertIn('relevance_explanation', response.json)

    # Mocking /ask endpoint with empty question
    @patch('flask_app.extract_llm_response_relevance_score')
    def test_ask_endpoint_empty_question(self, mock_extract_llm_response_relevance_score):
        mock_extract_llm_response_relevance_score.return_value = ('rewritten_question', 'llm_response', 'relevance', 'relevance_expl')
        response = self.app.post('/ask', json={'question': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    # Mocking /feedback endpoint
    @patch('flask_app.save_feedback')
    def test_feedback_endpoint_success(self, mock_save_feedback):
        mock_save_feedback.return_value = None
        response = self.app.post('/feedback', json={'question_uuid': '123', 'feedback': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    # Mocking /feedback endpoint with invalid feedback
    @patch('flask_app.save_feedback')
    def test_feedback_endpoint_invalid_feedback(self, mock_save_feedback):
        mock_save_feedback.return_value = None
        response = self.app.post('/feedback', json={'question_uuid': '123', 'feedback': 2})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    # Mocking /recent_questions endpoint
    @patch('flask_app.get_recent_questions')
    def test_recent_questions_endpoint(self, mock_get_recent_questions):
        mock_get_recent_questions.return_value = [{'question': 'Question 1'}, {'question': 'Question 2'}]
        response = self.app.get('/recent_questions')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


if __name__ == '__main__':
    unittest.main()