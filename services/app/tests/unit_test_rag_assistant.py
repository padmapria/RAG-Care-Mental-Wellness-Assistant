# tests/unit_test_rag_assistant.py
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app_directory = os.path.join(project_root, 'app')
sys.path.append(app_directory)

import unittest
from unittest.mock import patch, MagicMock
from rag_assistant import extract_llm_response_relevance_score

class TestRagAssistant(unittest.TestCase):

    @patch('rag_assistant.openai_4o')
    @patch('rag_assistant.rag')
    @patch('rag_assistant.openai_3_5')
    def test_extract_llm_response_relevance_score(self, mock_openai_3_5, mock_rag, mock_openai_4o):
        # Mock return values
        original_query = 'Original query'
        rewritten_query = 'Rewritten query'
        mock_openai_3_5.return_value = rewritten_query
        mock_rag.return_value = 'LLM answer'
        mock_openai_4o.return_value = '{"Relevance": "RELEVANT", "Explanation": "Explanation"}'

        # Call the function
        result = extract_llm_response_relevance_score(original_query)

        # Assertions
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        self.assertNotEqual(result[0], original_query)  # Ensure original query != rewritten query
        self.assertEqual(result[0], rewritten_query)
        self.assertEqual(result[1], 'LLM answer')  # Mock LLM answer
        self.assertEqual(result[2], 'RELEVANT')  # Mock Relevance
        self.assertEqual(result[3], 'Explanation')  # Mock Explanation


if __name__ == '__main__':
    unittest.main()