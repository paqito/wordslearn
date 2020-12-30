from wordslearn.models import WordEng
from wordslearn.models import WordPol

from wordsData import process_file
# from googletrans import Translator
from PyDictionary import PyDictionary

global translator

dictionary=PyDictionary()
# read input file
def readFile(fileName):
    print("Starting to read file with data {}".format(fileName))

def testData():
    entry = WordEng.objects.get(pk=1)
    print(entry)

# add pair of words
def addWord(engWord, polWord):

    if engWord is None or polWord is None:
        print("Missing word.")
        return

    # check if word exists
    existing_word = WordEng.objects.filter(word__exact=engWord)
    if existing_word:
        print("Word already exists {}. Skipping to add {}".format(existing_word, engWord))
        return

    word_instance = WordEng.objects.create(word=engWord)
    word_instance.save()

    # word_meaning = dictionary.meaning(word_instance.word)
    # print(word_meaning)
    # word_type = word_meaning.keys()
    # print("Word type {}".format(word_type))

    # check polish word
    wPol = None
    existing_word = WordPol.objects.filter(word__exact=polWord)
    if existing_word:
        print("Polish word exists in database")
        wPol = existing_word
    else:
        wPol = WordPol.objects.create(word=polWord)
        wPol.save()

    # add m2m relation
    word_instance.wordpol_set.add(wPol)

# add english word to database
def addEnglishWord(engWord = None):

    if engWord is None:
        print("Missing word.")
        return

    # check if word exists
    existing_word = WordEng.objects.filter(word__exact=engWord)
    if existing_word:
        print("Word already exists {}. Skipping to add {}".format(existing_word, engWord))
        return

    word_instance = WordEng.objects.create(word=engWord)
    word_instance.save()

    translator = Translator()
    result = translator.translate(engWord, src='en', dest='pl')
    print("Translation of {} is {}".format(engWord, result))

    wPol = WordPol.objects.create(word=result)
    wPol.save()

    # add m2m relation
    word_instance.wordpol_set.add(wPol)

def feed():
    input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    print("Starting to feed data")

    words_dictionary = process_file.readFileContent(input_file)
    print("words_dictionary: {}".format(words_dictionary))

    # add word to database
    for wEng, wPol in words_dictionary.items():
        addWord(wEng, wPol)

    # print("Print all eng words")
    # engWords = WordEng.objects.all()
    # print(engWords)
    print("Database feed done! {} words added".format(len(words_dictionary.keys())))