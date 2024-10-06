# tests/unit_test_db.py
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app_directory = os.path.join(project_root, 'app')
sys.path.append(app_directory)

# tests/test_db.py
import unittest
from unittest.mock import patch, MagicMock
from db import (
    get_mysql_connection,
    save_question,
    save_feedback,
    get_recent_questions
)
import mysql.connector
from datetime import datetime


class TestDBFunctions(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_get_mysql_connection(self, mock_connect):
        mock_connect.return_value = MagicMock()
        conn = get_mysql_connection()
        self.assertIsNotNone(conn)

    @patch('mysql.connector.connect')
    def test_get_mysql_connection_failure(self, mock_connect):
        mock_connect.side_effect = mysql.connector.Error
        with self.assertRaises(mysql.connector.Error):
            get_mysql_connection()

    @patch('db.get_mysql_connection')
    def test_save_question(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        save_question('1', 'Question', 'User Question', 10, 'Answer', 'Model', 1.0, 0.8, 'Relevance Expl')

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('db.get_mysql_connection')
    def test_save_question_failure(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error

        save_question('1', 'Question', 'User Question', 10, 'Answer', 'Model', 1.0, 0.8, 'Relevance Expl')

        mock_conn.commit.assert_not_called()

    @patch('db.get_mysql_connection')
    def test_save_feedback(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        save_feedback('1', 1)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('db.get_mysql_connection')
    def test_save_feedback_failure(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error

        save_feedback('1', 1)

        mock_conn.commit.assert_not_called()

    @patch('db.get_mysql_connection')
    def test_get_recent_questions(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'Question', 'User Question')]
        mock_cursor.description = [('id',), ('question',), ('user_question',)]

        result = get_recent_questions()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    @patch('db.get_mysql_connection')
    def test_get_recent_questions_failure(self, mock_get_mysql_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_mysql_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error

        result = get_recent_questions()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()