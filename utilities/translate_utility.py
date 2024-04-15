#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
    Module to translate input of words as a collection (dictionary, list)

    translate_word - main functions uses different translation modules to translate the word
    Uses different translation modules:
    PyDictionary
    googletrans.Translator
    Translator

    Return: collection of translated words as WordDetail
'''

import os
import json
# global translator
import processfile_utility
from processfile_utility import readFileContent

from translate import Translator
from google_translator import GoogleTranslator
from python_translator import TranslatorPython

class WordDetail:
    '''
        Class storing detailed information about translated world
    '''
    word = ""
    synonym = ""
    antonym = ""
    #type = ""
    translation = ""
    #definition = ""
    '''
        type_to_meaning - dictionary storing type of word and meaning
        verb, noun, adjective, adverb - and its list of meanings
    '''
    type_to_meaning = {}

    def __init__(self, word="", synonym="", antonym="", translation=""):
        self.word = word
        #self.definition = definition
        self.synonym = synonym
        self.antonym = antonym
        #self.type = type
        self.translation = translation
        self.type_to_meaning = {}

    def __str__(self):
        word_detail = f'WordDetail: {self.word}, translation:{self.translation}, synonym:{self.synonym}, antonym:{self.antonym} \n'
        for type, meaning in self.type_to_meaning.items():
            word_detail += f'type:{type}, meaning:{meaning}\n'

        return word_detail
    
    def get_json_string(self):      
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add_meanings(self, type, meanings):
        if self.type_to_meaning.get(type) is None:
            self.type_to_meaning[type] = meanings
        else:
            # append meaning if different
            for meaning in meanings:
                # trim meaning
                meaning = meaning.strip()
                if meaning not in self.type_to_meaning[type]:
                    self.type_to_meaning[type].append(meaning)
                else:
                    print("Meaning \"{}\" already exists".format(meaning))
    
    def is_meaning_exists(self, type, meaning):
        if self.type_to_meaning.get(type) is not None:
            if meaning in self.type_to_meaning[type]:
                return True
        return False

    def update_word_detail(self, word_detail):
        if word_detail.word != self.word:
            print("ERROR word not the same")
            return
        self.synonym = word_detail.synonym
        self.antonym = word_detail.antonym
        self.translation = word_detail.translation

        for type, meanings in word_detail.type_to_meaning.items():
            self.add_meanings(type, meanings)

    def from_json(self, json_string):
        word_detail = json.loads(json_string)
        #print("from_json {}".format(word_detail))
        self.word = word_detail["word"]
        self.translation = word_detail["translation"]
        self.synonym = word_detail["synonym"]
        self.antonym = word_detail["antonym"]
        #self.type = word_detail["type"]
        #self.definition = word_detail["definition"]
        self.type_to_meaning = word_detail["type_to_meaning"]


def dump_word_details_to_json(list_of_words, file_name):
    """
    dump_word_details_to_json - dump list of words to json file
    data {} stores dictionary of word and its WordDetail

    """
    print("dump_word_details_to_json")
    data = {}
    for wordDetail in list_of_words:
        if data.get(wordDetail.word) is None:
            data[wordDetail.word] = wordDetail
        else:
            # update existing word
            print("Updating word {}".format(wordDetail.word))
            data[wordDetail.word].update_word_detail(wordDetail)

    # append to exising json
    if os.path.exists(file_name) and not os.stat(file_name).st_size == 0:
        with open(file_name, 'r') as json_file:
            existing_data = json.load(json_file)
        if len(existing_data) > 0:
            for word, word_detail_json in existing_data.items():
                word_detail = WordDetail()
                word_detail.from_json(word_detail_json)
                
                if data.get(word) is None:
                    data[word] = word_detail
                else:
                    # update existing word
                    data[word].update_word_detail(word_detail)

    json_data = {}
    for word, word_detail in data.items():
        json_data[word] = word_detail.get_json_string()

    # dump data to json
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file)


class WordTranslator:
    '''
        Factory class to create different translators
    '''
    def __init__(self):
        self.googleTranslator = GoogleTranslator()
        self.translatorPython = TranslatorPython()
        '''
            translated_WordDetail_dict - dictionary storing translated words to details

        '''
        self.translated_WordDetail_dict = {}

    def set_translated_WordDetail_dict(self, json_file):
        '''
            json file contains dictionaty of key word and list of details word
        '''
        self.translated_WordDetail_dict = {}

        # check if file exists
        if not os.path.exists(json_file):
            print("WARNING file not found {} creating empty dict".format(json_file))
            return

        with open(json_file, 'r') as json_file:
            dict_of_words = json.load(json_file)
        
        for word, word_detail_json in dict_of_words.items():
            word_detail_obj = WordDetail()
            word_detail_obj.from_json(word_detail_json)
            if self.translated_WordDetail_dict.get(word) is None:
                self.translated_WordDetail_dict[word] = word_detail_obj
            else:
                self.translated_WordDetail_dict[word].update_word_detail(word_detail_obj)

    def save_translated_WordDetail_dict(self, json_file_name):
        '''
            save_translated_WordDetail_dict - save translated_WordDetail_dict to json file
        '''
        pass
        #dump_word_details_to_json(self.translated_WordDetail_dict, json_file_name)


    def add_word_to_translated_WordDetail_dict(self, word, word_detail):
        if self.translated_WordDetail_dict.get(word) is None:
            self.translated_WordDetail_dict[word] = word_detail
        else:
            self.translated_WordDetail_dict[word].update_word_detail(word_detail)
            
    def check_translation_exists(self, word_eng):
        if word_eng in self.translated_WordDetail_dict:
            return True
        return False
    
    def check_meaning_exists(self, word_eng, type="", meaning = ""):
        if word_eng in self.translated_WordDetail_dict:
            word_detail = self.translated_WordDetail_dict[word_eng]
            if len(word_detail.type_to_meaning) == 0:
                return False
            if word_detail.is_meaning_exists.get(type) is None:
                return False
            else:
                return word_detail.is_meaning_exists(type, meaning)
        return False

    def translate_word_googletrans(self, word_eng):
        
        list_of_words = []
        result = self.googleTranslator.translate(word_eng)
        if result:
            word = WordDetail(word=word_eng, translation=result.text)
            list_of_words.append(word)
        
        self.add_word_to_translated_WordDetail_dict(word_eng, word)
        return list_of_words
    
    def translate_word_pydictionary(self, word_eng, word_pol = ""):

        words_details = []
        word_eng, translation = self.translatorPython.translate_word(word_eng, word_pol)

        word_detail = WordDetail(word=word_eng, translation=translation, synonym="", antonym="")
        words_details.append(word_detail)

        self.add_word_to_translated_WordDetail_dict(word_eng, translation)

        return words_details
    
    def translate_by_translate(word_eng, word_pol = ""):

        print("Translation by translate disabled")
        return []
        list_of_words = []
        print("translate_by_translate wEng: {} wPol: {}".format(word_eng, word_pol))

        translator = Translator(to_lang="pl")
        translation = translator.translate(word_eng)

        word = WordDetail(word=word_eng, translation=translation, synonym=None, antonym=None, type=None, definition=None)
        list_of_words.append(word)

        return list_of_words


    def find_word_definition(self, word_eng):

        print("find_word_definition wEng: {}".format(word_eng))               
        words_type_definiton = self.translatorPython.find_meaning(word_eng)
        print("words_type_definiton {}".format(words_type_definiton))
        return words_type_definiton
    
    def set_definition_for_worddetail(self, word_detail, words_type_definiton):
        
        for type, meaning in words_type_definiton.items():
            word_detail.add_meanings(type, meaning)

    def set_definition(self, word_eng):
        if word_eng in self.translated_WordDetail_dict:
            for word_detail in self.translated_WordDetail_dict[word_eng]:
                if len(word_detail.type_to_meaning) == 0:
                    type_to_definition = self.find_word_definition(word_eng)
                    if len(type_to_definition) > 0:
                        self.set_definition_for_worddetail(word_detail, type_to_definition)
        else:
            print("ERROR word not found in translated_WordDetail_dict {}".format(word_eng))
        

    '''
    translate_word - main functions uses different translation modules to translate the word
    Returns list of translated WordDetail
    '''
    def translate_word(self, word_eng, srd='en', dest='pl'):

        list_of_words = []

        if self.check_translation_exists(word_eng):
            print("Translation exists skipping {}".format(word_eng))
            return list_of_words
    
        words = self.translate_word_googletrans(word_eng)
        if len(words) > 0:
            list_of_words = list_of_words + words
            print("Translation by google translate found")
            return list_of_words

        words = self.translate_word_pydictionary(word_eng)
        if len(words) > 0:
            list_of_words = list_of_words + words
            print("Translation by pydictionary found")
            return list_of_words

        words = self.translate_by_translate(word_eng)
        if len(words) > 0:
            list_of_words = list_of_words + words
            print("Translation by translate found")
            print(list_of_words)
            return list_of_words

        return list_of_words


# def translate_by_translate_test(words_dictionary):
#     print("translate_test")
#     list_of_words = []

#     for wEng, wPol in words_dictionary.items():
#         new_words = translate_by_translate(wEng, wPol)
#         list_of_words = list_of_words + new_words

#     return list_of_words


def save_to_json_file(list_of_words, file_name):
    print("save_to_json_file")
    with open(file_name, 'w') as json_file:
        json.dump(list_of_words, json_file)

def test_worddetail_to_json():
    print("TEST test_worddetail_to_json")
    word_detail = WordDetail(word="apple", translation="jabłko", synonym="syninim_test", antonym="anotnijm_test", type="type_test", definition="owoc")
    print(word_detail.get_json_string())




def test_exisitng_word_in_json():
    print("TEST test_exisitng_word_in_json")

    wordTranslator =  WordTranslator()
    wordTranslator.set_translated_WordDetail_dict("test_exist_in_json.json")

    result = wordTranslator.check_translation_exists("apple")
    if result:
        print("CORRECT Translation exists")
    else:
        print("ERROR Translation should exists")

def test_single_translation():
    print("TEST test_single_translation")
    wordTranslator =  WordTranslator()
    wordTranslator.set_translated_WordDetail_dict("test_exist_in_json.json")
    result = wordTranslator.translate_word("apple")
    if len(result) > 0:
        print("ERROR Translation should be skipped of exisiting word")
    result = wordTranslator.translate_word("grape")
    if len(result) == 0:
        print("ERROR Translation should be found of new word")
    
    print("Translated word {}".format(result))

def test_add_meaning():
    print("TEST test_add_meaning")
    word_detail1 = WordDetail(word="apple", translation="jabłko", synonym="syninim_test", antonym="anotnijm_test", type="type_test", definition="owoc 1")
    wordTranslator =  WordTranslator()
    print("word {}".format(word_detail1))

    type_to_definition = wordTranslator.find_word_definition("apple")
    print("type_to_definition {}".format(type_to_definition))
    wordTranslator.set_definition_for_worddetail(word_detail1, type_to_definition)
    print("word {}".format(word_detail1))

    wordTranslator.set_definition_for_worddetail(word_detail1, type_to_definition)
    print("word {}".format(word_detail1))


def main():

    print("Main Running translatorModule script")
    #input_file = r"D:\Programming\DjangoProjects\Words\words\wordsData\test_words.txt"
    #input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    #input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\test_words_english.txt"
    input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\game_words.txt"
    #input_file = r"D:\Programming\DjangoProjects\Words\words\wordsData\test_game_word.txt"
    words_dictionary = processfile_utility.readFileContent(input_file)

    print("words_dictionary len : {}".format(len(words_dictionary)))
    print("words_dictionary : {}".format(words_dictionary))

    #test_worddetail_to_json()
    #translated_words_details = translate_word_test(words_dictionary)

    # test_exisitng_word_in_json()
    # test_single_translation()
    # test_add_meaning()

    wordTranslator = WordTranslator()
    # wordTranslator.set_translated_WordDetail_dict("words_already_translated.json")
    json_database_file = "result_with_definition_already_translated.json"
    wordTranslator.set_translated_WordDetail_dict(json_database_file)

    word_details = []
    for word_eng, word_pol in words_dictionary.items():
        words = wordTranslator.translate_word(word_eng)
        for word in words:
            word_details.append(word)


    #wordTranslator.save_translated_WordDetail_dict(json_database_file)
    dump_word_details_to_json(word_details, "resul_already_translated.json")
    dump_word_details_to_json(word_details, "result_with_definition_already_translated.json")

    # find meaning for word
    for word_detail in word_details:
        if wordTranslator.check_meaning_exists(word_detail.word) is False:
            type_to_definition = wordTranslator.find_word_definition(word_detail.word)
            wordTranslator.set_definition_for_worddetail(word_detail, type_to_definition)

    dump_word_details_to_json(word_details, "result_with_definition_already_translated.json")
    #wordTranslator.save_translated_WordDetail_dict(json_database_file)

    
    # for word_eng, word_pol in words_dictionary.items(): 
    #     wordTranslator.set_definition(word_eng)

    #wordTranslator.set_translated_WordDetail_dict("test_exist_in_json.json")

    #list_of_translation = wordTranslator.translate_dict(words_dictionary)    
    #print("result of translate_dict {} words".format(len(list_of_translation)))
    #for word in list_of_translation:
    #    print(word)

    # print("------------------------pydictionary_test------------------------------------")
    # list_of_words = pydictionary_test(words_dictionary)
    # print("result of pydictionary_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print("##")
    #     print(w)
    
    # save_to_json_file(list_of_words, "pydictionary_test.json")

    # print("----------------------------googletrans_test--------------------------------")
    #googleTranslator = GoogleTranslator()

    #
    # print("----------------------------translate_by_translate_test--------------------------------")
    # list_of_words = translate_by_translate_test(words_dictionary)
    # print("result of translate_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print(w)
    #     print("##")

    # print("------------------------------------------------------------")
    # list_of_words = translate_word_test(words_dictionary)
    # print("result of translate_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print(w)
    #     print("##")

    #print("-----------------SINGLE WORLD ------------------------------------")
    #list_of_words = translate_word("impeccable", "")
    #print(list_of_words)

    # print("-----------------SINGLE WORLD TranslatorPython------------------------------------")
    # translatorPythonSingle = TranslatorPython()
    # print(translatorPythonSingle.translate_word("obtuse", ""))

    # for w in list_of_words:
    #     print(w)
        # list_of_words = googletrans_test(words_dictionary)
    # print("result of googletrans_test {} words".format(len(list_of_words)))

if __name__ == "__main__":
    main()
