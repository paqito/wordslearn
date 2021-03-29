#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
    Module to translate input of words as a collection (dictionary, list)

    translate_words - main functions uses different translation modules to translate the word
    Uses different translation modules:
    PyDictionary
    googletrans.Translator
    Translator

    Return: collection of translated words as WordDetail
'''

import os
import json
# global translator
# import processfile_utility
from PyDictionary import PyDictionary
from googletrans import Translator as googleTranslator
from translate import Translator


class Translator:
        def translate(self):
            pass

class TranslatorPython(Translator):

    pydictionary = None

    def __init__(self):
        pydictionary = PyDictionary()

    def translate(self):
            pass

'''
    Class storing detailed information about translated world
'''
class WordDetail:
    word = ""
    synonym = ""
    antonym = ""
    type = ""
    translation = ""
    definition = ""

    def __init__(self, word="", definition="", synonym="", antonym="", type="", translation=""):
        self.word = word
        self.definition = definition
        self.synonym = synonym
        self.antonym = antonym
        self.type = type
        self.translation = translation

    def __str__(self):
        return f'WordDetail: {self.word}, type:{self.type}, translation:{self.translation}, synonym:{self.synonym}, antonym:{self.antonym}, definition:{self.definition}'

'''
translate_words - main functions uses different translation modules to translate the word
Returns list of translated WordDetail
'''
def translate_words(word_eng, word_pol = ""):
    list_of_words = []

    words = translate_words_pydictionary(word_eng, word_pol)
    if len(words) > 0:
        list_of_words = list_of_words + words
        return list_of_words

    words = translate_by_translate(word_eng, word_pol)
    if len(words) > 0:
        list_of_words = list_of_words + words
        return list_of_words

    return list_of_words

def translate_words_pydictionary(word_eng, word_pol = ""):
    print("Translation by pydictionary")
    pydictionary = PyDictionary()

    list_of_words = []

    #TODO trim results
    number_of_words = 5
    synonyms = pydictionary.synonym(word_eng)
    antonyms = pydictionary.antonym(word_eng)

    synonym_tab = synonyms[:number_of_words]
    antonym_tab = antonyms[:number_of_words]
    synonym = synonym_tab[:number_of_words] if len(synonym_tab) > number_of_words else synonym_tab[:len(synonym_tab)]
    antonym = antonym_tab[:number_of_words] if len(antonym_tab) > number_of_words else antonym_tab[:len(antonym_tab)]

    translation = pydictionary.translate(word_eng, 'pl')

    if not translation:
        if word_pol == "":
            print("Warning no translation found")
        translation = word_pol

    print("translate_words_pydictionary wEng: {} translation: {}".format(word_eng, translation))
    meanings = pydictionary.meaning(word_eng)
    for key, value in meanings.items():
        print("key {}  value {}".format(key, value))
        word = WordDetail(word=word_eng, translation=translation, synonym=synonym, antonym=antonym, type=key, definition=value)
        list_of_words.append(word)

    return list_of_words

def translate_word_googletrans(word_eng, word_pol = ""):
    print("Translatio by googletrans")
    retry_count = 3
    list_of_words = []
    googleTranslator = googleTranslator()
    print("translate_word_googletrans wEng: {} wPol: {}".format(word_eng, word_pol))
    result = None

    while retry_count > 0:
        try:
            result = googleTranslator.translate(word_eng, src='en', dest='pl')
            # result = googleTranslator.translate(word_eng, src='en', dest='pl')
            break
        except json.decoder.JSONDecodeError:
            print("Exception found")
            retry_count = retry_count - 1

    if result:
        print(str(result.text))
    else:
        print("No translation found for {}".format(word_eng))

    return list_of_words

def translate_by_translate(word_eng, word_pol = ""):
    print("Translatio by translate")
    list_of_words = []
    print("translate_by_translate wEng: {} wPol: {}".format(word_eng, word_pol))

    translator = Translator(to_lang="pl")
    translation = translator.translate(word_eng)

    word = WordDetail(word=word_eng, translation=translation, synonym=None, antonym=None, type=None, definition=None)
    list_of_words.append(word)

    return list_of_words


def pydictionary_test(words_dictionary):

    print("pydictionary_test")
    list_of_words = []

    for wEng, wPol in words_dictionary.items():

        new_words = translate_words_pydictionary(wEng, wPol)
        list_of_words = list_of_words + new_words

    return list_of_words

def googletrans_test(words_dictionary):
    print("googletrans_test")
    list_of_words = []

    for wEng, wPol in words_dictionary.items():
        new_words = translate_word_googletrans(wEng, wPol)
        list_of_words = list_of_words + new_words

    return list_of_words

def translate_by_translate_test(words_dictionary):
    print("translate_test")
    list_of_words = []

    for wEng, wPol in words_dictionary.items():
        new_words = translate_by_translate(wEng, wPol)
        list_of_words = list_of_words + new_words

    return list_of_words

def translate_words_test(words_dictionary):
    print("translate_words_test")
    list_of_words = []

    for wEng, wPol in words_dictionary.items():
        new_words = translate_words(wEng, wPol)
        list_of_words = list_of_words + new_words

    return list_of_words

def main():

    print("Main Running translatorModule script")
    input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    print("Starting to feed data")
    #
    words_dictionary = processfile_utility.readFileContent(input_file)

    print("words_dictionary len : {}".format(len(words_dictionary)))
    print("words_dictionary : {}".format(words_dictionary))

    # print("------------------------------------------------------------")
    # list_of_words = pydictionary_test(words_dictionary)
    # print("result of pydictionary_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print(w)
    #     print("##")
    #
    # print("------------------------------------------------------------")
    # list_of_words = translate_by_translate_test(words_dictionary)
    # print("result of translate_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print(w)
    #     print("##")

    # print("------------------------------------------------------------")
    # list_of_words = translate_words_test(words_dictionary)
    # print("result of translate_test {} words".format(len(list_of_words)))
    # for w in list_of_words:
    #     print(w)
    #     print("##")

    print("-----------------SINGLE WORLD ------------------------------------")
    list_of_words = translate_words("impeccable", "")
    print(list_of_words)
    # for w in list_of_words:
    #     print(w)
        # list_of_words = googletrans_test(words_dictionary)
    # print("result of googletrans_test {} words".format(len(list_of_words)))

if __name__ == "__main__":
    main()
