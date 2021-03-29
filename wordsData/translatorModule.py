#!/usr/bin/env python
# -*- coding: utf8 -*-

# from googletrans import Translator
import os
from PyDictionary import PyDictionary
import processFile
global translator

pydictionary=PyDictionary()

class Translator:
        def translate(self):
            pass

class TranslatorPython(Translator):

    pydictionary = None

    def __init__(self):
        pydictionary = PyDictionary()

    def translate(self):
            pass


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
        return f'WordDetail: {self.word}, {self.type}, {self.translation}, {self.synonym}, {self.antonym}, {self.definition}'

def translate_words(word_eng, word_pol = ""):

    list_of_words = []
    print("translate_words wEng: {} wPol: {}".format(word_eng, word_pol))

    synonym = pydictionary.synonym(word_eng)
    antonym = pydictionary.antonym(word_eng)
    translation = pydictionary.translate(word_eng, 'pl')

    if not translation:
        if word_eng == "":
            print("Warning no translation found")
        translation = word_pol

    # print("synonym {}".format(synonym))
    # print("translation {}".format(translation))

    meanings = pydictionary.meaning(word_eng)
    for key, value in meanings.items():
        word = WordDetail(word=word_eng, translation=translation, synonym=synonym, antonym=antonym, type=key, definition=value)
        list_of_words.append(word)

    return list_of_words

def pydictionary_test(words_dictionary):

    print("pydictionary_test")
    eng_pol_dictionary = {}
    list_of_words = []

    for wEng, wPol in words_dictionary.items():

        new_words = translate_words(wEng, wPol)
        list_of_words = list_of_words + new_words

    return list_of_words

def main():

    print("Main Running translatorModule script")
    input_file = "D:\Programming\DjangoProjects\Words\words\wordslearn\wordsData\wordsEnglish.txt"
    print("Starting to feed data")

    words_dictionary = processFile.readFileContent(input_file)
    # print("words_dictionary: {}".format(words_dictionary))

    list_of_words = pydictionary_test(words_dictionary)
    print("result of {} words".format(len(list_of_words)))
    for w in list_of_words:
        print("------------")
        print(w)

if __name__ == "__main__":
    main()
