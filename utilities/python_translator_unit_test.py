import unittest

import python_translator

class TestPythonTranslator(unittest.TestCase):
    
    def setUp(self):
        self.translator = python_translator.PythonTranslator()
    
    def test_translate_word(self):      
        word_eng = 'dog'
        word_pol = 'pies'
        word_eng, translation = self.translator.translate_word(word_eng, word_pol)
        self.assertEqual(word_eng, 'dog')
        self.assertEqual(translation, 'pies')
    
    def test_find_meaning(self):
        word_eng = 'dog'
        meanings = self.translator.find_meaning(word_eng)
        self.assertTrue(len(meanings) > 0)

if __name__ == '__main__':
    unittest.main()