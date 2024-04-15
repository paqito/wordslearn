"""
unit tests for google_translator.py
"""

import unittest

from words.utilities.google_translator import GoogleTranslator

class TestGoogleTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = GoogleTranslator()
        self.translator.request_count = 0
        # create a file with request count
        self.translator.request_file_name = "test_request_count_google.txt"

    def tearDown(self):
        self.translator.save_request_count_to_file()
    
    def test_translate(self):
        init_request_count = self.translator.request_count

        result  = self.translator.translate("apple", src='en', dest='pl')
        self.assertIsNotNone(result)
        self.assertEqual(result.text, "jabłko")
        self.assertGreater(self.translator.request_count, init_request_count)


    def test_read_request_count_from_file(self):
        self.translator.request_count = -1
        self.translator.read_request_count_from_file()
        self.assertGreaterEqual(self.translator.request_count, 0)
    

if __name__ == '__main__':
    unittest.main()