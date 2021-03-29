from wordslearn.models import WordEng
from wordslearn.models import WordPol

from wordsData import processFile
# from googletrans import Translator
from PyDictionary import PyDictionary

global translator

pydictionary=PyDictionary()
# read input file
def readFile(fileName):
    print("Starting to read file with data {}".format(fileName))

def testData():
    entry = WordEng.objects.get(pk=1)
    print(entry)

# add pair of words
def addWordToDatabase(engWord, polWord):

    if engWord is None or polWord is None:
        print("Missing word.")
        return

    engWordInstance = None
    # check if Eng word exists
    # eng_in_db = WordEng.objects.filter(word__exact=engWord)
    print("Checking {} in english words".format(engWord))
    eng_in_db = WordEng.objects.filter(word__exact=engWord).first()
    if eng_in_db:
        print("Word already exists {}. Skipping to add {}".format(eng_in_db, engWord))
        engWordInstance = existing_word
    else:
        print("Create new Eng instance")
        engWordInstance = WordEng.objects.create(word=engWord)
        engWordInstance.save()

    # word_meaning = dictionary.meaning(word_instance.word)
    # print(word_meaning)
    # word_type = word_meaning.keys()
    # print("Word type {}".format(word_type))

    # check polish word
    polWordInstance = None
    # pol_in_db = WordPol.objects.filter(word__exact=polWord)
    print("Checking {} in polish words".format(polWord))
    pol_in_db = WordPol.objects.filter(word__exact=polWord).first()
    if pol_in_db:
        print("Polish word exists in database")
        polWordInstance = pol_in_db
    else:
        print("Create new Pol instance")
        polWordInstance = WordPol.objects.create(word=polWord)
        polWordInstance.save()

    # adding two new words eng and pol
    if not eng_in_db and not pol_in_db:
        engWordInstance.wordpol_set.add(polWordInstance)
    # add new polish meaning to eng word
    elif eng_in_db and not pol_in_db:
        print("Adding {} to {} ".format(polWordInstance, engWordInstance))
        engWordInstance.wordpol_set.add(polWordInstance)
        # add new english meaning to pol word
    elif not eng_in_db and pol_in_db:
        print("Adding {} to {} ".format(engWordInstance, polWordInstance))
        polWordInstance.wordsEng.add(engWordInstance)
    else:
        print("WARNING Unknown state engWordInstance:{} polWordInstance:{}".format(engWordInstance, polWordInstance))

    # add m2m relation
    # word_instance.wordpol_set.add(wPol)

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

def pydictionary_test(words_dict):


    print("pydictionary_test")

    for wEng, wPol in words_dictionary.items():
        print("wEng: {} wPol: {}".format(wEng, wPol))

        print(pydictionary.meaning(wEng))
        print(pydictionary.synonym(wEng))
        print(pydictionary.translate(wEng, 'pl'))


def feed():
    input_file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    print("Starting to feed data")

    words_dictionary = processFile.readFileContent(input_file)
    print("words_dictionary: {}".format(words_dictionary))

    # add word to database
    for wEng, wPol in words_dictionary.items():
        print("Addind wEng: {} wPol: {}".format(wEng, wPol))
        addWordToDatabase(wEng, wPol)

    # print("Print all eng words")
    # engWords = WordEng.objects.all()
    # print(engWords)
    print("Database feed done! {} words added".format(len(words_dictionary.keys())))


def main():
    print("Main Running feedData script")

# remove previous data
print("Remove previous data")
WordEng.objects.all().delete()
WordPol.objects.all().delete()

print("Running feedData script")
feed()

if __name__ == "__main__":
    main()

