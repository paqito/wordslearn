
import os
import sys

from PyDictionary import PyDictionary

class Translator:
        
    def __init__(self):
        self.request_count = 0
        self.request_file_name = 'request_count.txt'

    def translate(self):
        pass

    def __del__(self):
        print("Translator object destroyed")
        self.save_request_count_to_file()

    def read_request_count_from_file(self):
        self.request_count = 0
        if os.path.exists(self.request_file_name):
            with open(self.request_file_name, 'r') as f:
                self.request_count = int(f.read())

    def save_request_count_to_file(self):
        with open(self.request_file_name, 'w') as f:
            f.write(str(self.request_count))
    
    def increase_request_count(self):
        self.request_count = self.request_count + 1

class TranslatorPython(Translator):

    pydictionary = None

    def __init__(self):
        self.pydictionary = PyDictionary()
        self.request_file_name = 'request_count_python.txt'
        self.read_request_count_from_file()

    def translate(self):
        pass

    def translate_word(self, word_eng, word_pol = ""):

        self.increase_request_count()
        translation = self.pydictionary.translate(word_eng, 'pl')

        if not translation:
            if word_pol == "":
                print("Warning no translation found")
            translation = word_pol
        else:
            print("Translation found: {}".format(translation))

        return word_eng, translation

    def find_meaning(self, word_eng):

        self.increase_request_count()
        #print("Meaning of word: {}".format(word_eng))
        meanings = self.pydictionary.meaning(word_eng)
        #print("Meanings: {}".format(meanings))
        if meanings is not None and len(meanings) > 0:
            for type, meaning in meanings.items():
                print("type {}  meaning {}".format(type, meaning))
            return meanings
        else:
            print("No meaning found")
            return {}

    def find_synonyms(self, word_eng):
        synonyms = []
        try:
            self.increase_request_count()
            synonyms = self.pydictionary.synonym(word_eng)
            if synonyms is None:
                synonyms = []
        except Exception as e:
            print("Exception found: {}".format(e))
        
        #skip synonyms and antonyms for now
        number_of_words = 5
        antonyms = []

        synonym_tab = ' '.join(synonyms) if len(synonyms) > 0 else ''
        synonym_tab = synonyms[:number_of_words]
        synonym = synonym_tab[:number_of_words] if len(synonym_tab) > number_of_words else synonym_tab[:len(synonym_tab)]
        return synonyms

    def find_antonyms(self, word_eng):
        antonyms = []
        try:
            self.increase_request_count()
            antonyms = self.pydictionary.antonym(word_eng)
            if antonyms is None:
                antonyms = []
        except Exception as e:
            print("Exception found: {}".format(e))    

        antonym_tab = ' '.join(antonyms) if len(antonyms) > 0 else ''
        antonym_tab = antonyms[:number_of_words]
        antonym = antonym_tab[:number_of_words] if len(antonym_tab) > number_of_words else antonym_tab[:len(antonym_tab)]
        return antonyms

    # def createWordDetail(self, word_eng, translation, synonym_tab, antonym_tab):
    #     # print("translate_words_pydictionary wEng: {} translation: {}".format(word_eng, translation))
    #     meanings = self.pydictionary.meaning(word_eng)
    #     for type, meaning in meanings.items():
    #         #print("key {}  value {}".format(type, meaning))
    #         word = WordDetail(word=word_eng, translation=translation, synonym=synonym_tab, antonym=antonym_tab, type=type, definition=meaning)
    #         list_of_words.append(word)

    #     return list_of_words

# def translate_words_pydictionary(words = {}):
#     list_words_details = []

#     for word_eng, word_pol in words.items():
#         word_detail = translate_words_pydictionary(word_eng, word_pol)
#         list_words_details.append(word_detail)
    
#     return list_words_details



def main():
    translator = TranslatorPython()
    translator.translate_word("apple")
    translator.find_meaning("apple")
    translator.find_synonyms("apple")
    translator.find_antonyms

if __name__ == "__main__":

    main()