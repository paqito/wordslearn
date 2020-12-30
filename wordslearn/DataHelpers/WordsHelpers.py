from wordslearn.models import WordEng
from wordslearn.models import WordPol
from wordslearn.models import LanguageChoice

from datetime import datetime, timedelta

def getNumberOfWords(daysToSubstract=0, languague = LanguageChoice.EN):
    today = datetime.now()
    starting_date = today - timedelta(days=daysToSubstract)

    if WordEng.objects.exists():
        return WordEng.objects.filter(date_of_add__lt=starting_date).count()
    else:
        return None

def getLatestWord(numOfWords=5):
    if WordEng.objects.exists():
        words = WordEng.objects.order_by('-date_of_add')[:numOfWords]
        return words
    else:
        return None

def getLatestWordAdded():
    pass

def getNumberOfWordsInDataRange(daysToSubstract=7, languague = LanguageChoice.EN):
    words = []
    # todays date
    today = datetime.now()
    print(today)

    starting_date = today - timedelta(days=daysToSubstract)
    if languague == LanguageChoice.EN:
        words = WordEng.objects.filter(date_of_add__gt=starting_date)
    elif languague == LanguageChoice.PL:
        words = WordPol.objects.filter(date_of_add__gt=starting_date)

    return words