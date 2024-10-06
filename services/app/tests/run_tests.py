# tests/run_tests.py
import unittest
import logging
import os
from unittest import loader

## way1
def run_tests_():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting tests")
    suite = unittest.TestLoader().discover(os.path.dirname(__file__), pattern='unit_*.py')
    unittest.TextTestRunner().run(suite)
    
    suite = unittest.TestLoader().discover(os.path.dirname(__file__), pattern='integration_*.py')
    unittest.TextTestRunner().run(suite)
    
## way2
def run_tests():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting tests")
    
    # Load tests from specific files (make sure these files are in the current directory or within sys.path)
    test_files = [
        'unit_test_db',  # module name, not file name (without .py)
        'unit_test_rag_assistant',
        'unit_test_flask_app',
        'integration_test_flask_app'
    ]
    
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    # Load and add each test module to the suite
    for file in test_files:
        try:
            suite.addTests(loader.loadTestsFromName(file))
            logging.info(f"Loaded tests from {file}")
        except Exception as e:
            logging.error(f"Error loading {file}: {e}")
    
    # Run the test suite
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    run_tests()