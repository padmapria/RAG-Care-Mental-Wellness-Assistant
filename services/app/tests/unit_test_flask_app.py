# tests/unit_test_flask_app.py
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from flask import json

# Add the project root and app directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app_directory = os.path.join(project_root, 'app')
sys.path.append(app_directory)

from flask_app import app, save_feedback

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        
    @patch('flask_app.save_feedback')
    def test_feedback_endpoint(self, mock_save_feedback):
        mock_save_feedback.return_value = None

        response = self.client.post('/feedback', json={'question_uuid': '123', 'feedback': 1})

        mock_save_feedback.assert_called_once_with('123', 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Feedback submitted successfully')

    def test_ask_endpoint_error(self):
        # Test error handling
        response = self.client.post('/ask', json={'invalid': 'data'})
        self.assertEqual(response.status_code, 400)

    def test_ask_endpoint_no_question(self):
        # Test no question provided
        response = self.client.post('/ask', json={})
        self.assertEqual(response.status_code, 400)

    def test_feedback_endpoint_no_uuid(self):
        # Test no question UUID provided
        response = self.client.post('/feedback', json={'feedback': 1})
        self.assertEqual(response.status_code, 400)

    def test_feedback_endpoint_invalid_feedback(self):
        # Test invalid feedback value
        response = self.client.post('/feedback', json={'question_uuid': '123', 'feedback': 'invalid'})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()