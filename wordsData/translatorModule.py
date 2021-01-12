import process_file
# from googletrans import Translator
from PyDictionary import PyDictionary

global translator

pydictionary=PyDictionary()


def pydictionary_test(words_dictionary):

    print("pydictionary_test")

    for wEng, wPol in words_dictionary.items():
        print("------------------------------------")
        print("wEng: {} wPol: {}".format(wEng, wPol))

        print(pydictionary.meaning(wEng))
        print(pydictionary.synonym(wEng))
        print(pydictionary.translate(wEng, 'pl'))

def main():

    print("Main Running translatorModule script")
    input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    print("Starting to feed data")

    words_dictionary = process_file.readFileContent(input_file)
    print("words_dictionary: {}".format(words_dictionary))

    pydictionary_test(words_dictionary)

if __name__ == "__main__":
    main()
