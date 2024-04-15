"""
unit test for translate_utility.py
"""


import unittest
import os
import json
from words.utilities.translate_utility import WordTranslator
from words.utilities.translate_utility import WordDetail
from words.utilities.translate_utility import dump_word_details_to_json



class TestWordDetail(unittest.TestCase):
    """
    TestWordDetail class
    """
    def setUp(self):
        self.wordDetail = WordDetail(word="apple", translation="jabłko", synonym="synonim_test", antonym="anotnim_test")
    
    def test_add_meaning(self):
        """
        test add_meaning
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])
        # verify type_to_meaning size is 2
        self.assertEqual(len(self.wordDetail.type_to_meaning), 1)
        self.assertEqual(self.wordDetail.type_to_meaning, {'type_test_1': ['owoc 1']})
    
    def test_is_meaning_exists(self):
        """
        test is_meaning_exists
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1", "owoc 2"])
        self.assertTrue(self.wordDetail.is_meaning_exists("type_test_1", "owoc 1"))
        self.assertFalse(self.wordDetail.is_meaning_exists("type_test_1", "owoc 3"))
    
    def test_add_meaning_additional(self):
        """
        test add_meaning 2  times
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])
        self.wordDetail.add_meanings("type_test_2", ["owoc 2"])
        # verify type_to_meaning size is 2
        self.assertEqual(len(self.wordDetail.type_to_meaning), 2)
        self.assertEqual(self.wordDetail.type_to_meaning, {'type_test_1': ['owoc 1'], 'type_test_2': ['owoc 2']})
    
    def test_add_meaning_same_type(self):
        """
        test add_meaning 2  times
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])
        self.wordDetail.add_meanings("type_test_1", ["owoc 2"])
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])
        self.wordDetail.add_meanings("type_test_1", [" owoc 1 "])
        # verify type_to_meaning size is 2
        self.assertEqual(len(self.wordDetail.type_to_meaning), 1)
        self.assertEqual(self.wordDetail.type_to_meaning, {'type_test_1': ['owoc 1','owoc 2']})


    def test_update_word_detail(self):
        """
        test update_word_detail
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])

        new_word_detail = WordDetail(word="apple", translation="jabłko", synonym="synonim_test_1", antonym="anotnim_test_1")
        new_word_detail.add_meanings("type_test_1", ["owoc 2"])

        self.wordDetail.update_word_detail(new_word_detail)
        self.assertEqual(self.wordDetail.translation, "jabłko")
        self.assertEqual(self.wordDetail.synonym, "synonim_test_1")
        self.assertEqual(self.wordDetail.antonym, "anotnim_test_1")
        self.assertEqual(self.wordDetail.type_to_meaning, {'type_test_1': ['owoc 1', 'owoc 2']})
    
    def test_world_detail_to_json(self):
        """
        test world_detail_to_json
        """
        self.wordDetail.add_meanings("type_test_1", ["owoc 1"])
        self.wordDetail.add_meanings("type_test_1", ["owoc 1 inny"])
        self.wordDetail.add_meanings("type_test_2", ["owoc 2"])
        word_detail_json = self.wordDetail.get_json_string()
        # dump to file
        with open("test_dump_word_detail_to_json.json", 'w') as json_file:
            #json_file.write('{"apple": ' + word_detail_json + '}')
            json_file.write(word_detail_json)
        # assert file exists
        self.assertTrue(os.path.exists("test_dump_word_detail_to_json.json"))

    def test_json_to_worddetail(self):

        data = ""
        with open("test_json_to_word_detail.json", 'r') as json_file:
            data = json_file.read()
        
        self.assertNotEqual(data, "")
    
        word_detail = WordDetail()
        word_detail.from_json(data)

        self.assertEqual(word_detail.word, "apple")
        self.assertEqual(len(word_detail.type_to_meaning), 2)
        self.assertEqual(word_detail.type_to_meaning['type_test_1'][1], "owoc 1 inny")
        self.assertEqual(word_detail.type_to_meaning['type_test_2'][0], "owoc 2")        


class TestWordTranslator(unittest.TestCase):
    """
    TestWordTranslator class
    """
    def setUp(self):
        self.translator = WordTranslator()
    
    def test_translate(self):
        """
        test translate
        """
        result = self.translator.translate_word("apple", "en", "pl")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].translation, "jabłko")

    def test_translate_multiple(self):
        """
        test translate multiple
        """
        list_of_words = ["apple", "banana"]
        word_details = []
        for word in list_of_words:
            result = self.translator.translate_word(word, "en", "pl")
            word_details = word_details + result
        
        self.assertEqual(len(word_details), 2)
        # case insensitive assertation
        self.assertEqual(word_details[0].translation, "jabłko")
        self.assertEqual(word_details[1].translation, "banan")

        self.assertEqual(len(self.translator.translated_WordDetail_dict), 2)

    def test_translate_pydictionary(self):
        """
        test translate pydictionary
        """
        result = self.translator.translate_word_pydictionary("apple", "")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].translation, "jabłko")

    def test_translate_googletrans(self):
        """
        test translate googletrans
        """
        result = self.translator.translate_word_googletrans("apple")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].translation, "jabłko")

    def test_dump_to_json(self):
        """
        test dump_to_json
        """ 
        word_detail1 = WordDetail(word="apple", translation="jabłko", synonym="syninim_test", antonym="anotnijm_test")
        word_detail1.add_meanings("type_test_1", ["owoc 1"])
        word_detail1.add_meanings("type_test_2", ["owoc 2"])

        word_detail2 = WordDetail(word="orange", translation="pomarańcza", synonym="syninim_test", antonym="anotnijm_test")

        word_detail3 = WordDetail(word="banana", translation="banan", synonym="syninim_test", antonym="anotnijm_test")
        word_detail3.add_meanings("type_test_1", ["owoc 1"])
        word_detail3.add_meanings("type_test_1", ["owoc 2"])

        list_of_words = [word_detail1, word_detail2, word_detail3]

        dump_word_details_to_json(list_of_words, "test_dump_to_json.json")

        # verify file exists
        self.assertTrue(os.path.exists("test_dump_to_json.json"))
        
        os.remove("test_dump_to_json.json")
    
    def test_load_from_json(self):
        """
        test load_from_json
        """
        dict_of_words = {}
        with open("test_json_to_wordetails.json", 'r') as json_file:
            dict_of_words = json.load(json_file)
        
        print(dict_of_words)
        print(dict_of_words["apple"])

        for word, word_detail_json in dict_of_words.items():
            word_detail = WordDetail()
            word_detail.from_json(word_detail_json)
            dict_of_words[word] = word_detail
        
        self.assertEqual(len(dict_of_words), 3)
        self.assertEqual(dict_of_words["apple"].translation, "jabłko")
        self.assertEqual(dict_of_words["banana"].translation, "banan")
        self.assertEqual(dict_of_words["orange"].translation, "pomarańcza")
        self.assertEqual(dict_of_words["apple"].type_to_meaning["type_test_1"], ["owoc 1"])
    
    def test_load_from_json(self):
        """
        test load_from_json
        """
        dict_of_words = {}
        with open("test_result_with_definition.json", 'r') as json_file:
            dict_of_words = json.load(json_file)
        
        for word, word_detail_json in dict_of_words.items():
            word_detail = WordDetail()
            word_detail.from_json(word_detail_json)
            dict_of_words[word] = word_detail
        
        self.assertEqual(len(dict_of_words), 12)
        self.assertEqual(dict_of_words["Entertaining"].translation, "Rozrywkowy")
        self.assertEqual(dict_of_words["Addictive"].translation, "Wciągający")
        self.assertEqual(dict_of_words["Addictive"].type_to_meaning["Adjective"], ["causing or characterized by addiction"])


    def test_set_translated_WordDetail_dict(self):

        self.translator.set_translated_WordDetail_dict("test_result_with_definition.json")

        self.assertEqual(self.translator.translated_WordDetail_dict["Entertaining"].translation, "Rozrywkowy")
        self.assertEqual(len(self.translator.translated_WordDetail_dict), 12)
        





if __name__ == '__main__':
    unittest.main()
    