from django.db import models
from wordslearn import wordDefinitions

from enum import Enum

class LanguageChoice(Enum):
    EN = "English"
    PL = "Polish"


def create_eng_word(**kwarg):
    '''
    Creates WordEng Model object base on dictionary values

    :param **kwarg: keyqord argument to pass fields to create new model
    '''
    print("create_eng_word {}".format(kwarg.get('word', 'no word')))
    word_instance = WordEng()

    word_instance.word = kwarg['word']
    word_instance.definition = kwarg['definition']
    word_instance.synonym = kwarg['synonym']
    word_instance.antonym = kwarg['antonym']
    # polish_word = kwarg['translation']

    # convert wort_type to correct format
    translated_type = kwarg['type']
    print("translated_type {} {}".format(translated_type, translated_type.lower()))
    word_instance.word_type = wordDefinitions.wordType_conversion.get(translated_type.lower(), 'Other')
    print(word_instance.word_type)

    word_instance.save()

    print(str(word_instance))

    return word_instance

def create_pol_word(**kwarg):
    '''
    Creates WordPol Model object base on dictionary values

    :param **kwarg: keyqord argument to pass fields to create new model
    '''
    word_instance = WordPol()

    word_instance.word = kwarg['word']
    word_instance.definition = kwarg.get('definition', 'None')
    word_instance.synonym = kwarg.get('synonym', 'None')
    word_instance.antonym = kwarg.get('antonym', 'None')
    # word_instance.antonym = kwarg['antonym']

    translated_type = kwarg.get('type', 'Other')
    print("translated_type {}".format(translated_type))
    word_instance.word_type = wordDefinitions.wordType_conversion.get(translated_type.lower(), 'Other')
    word_instance.save()

    print(str(word_instance))

    return word_instance

# Create your models here.
class Word(models.Model):

    word = models.CharField(max_length=200, null=False, help_text='Enter the word')
    date_of_add = models.DateTimeField(auto_now=True, blank=True, help_text='date added')

    definition = models.CharField(max_length=200, blank=True, null=False, help_text='Enter the definition of english word')
    synonym = models.CharField(max_length=200, blank=True, null=False, help_text='Enter the synonym of english word')
    antonym = models.CharField(max_length=200, blank=True, null=False, help_text='Enter the antonym of english word')

    class Meta:
        abstract = True
        ordering = ["word"]

    def __str__(self):
        string_representation = "{} {} {} {} ".format(self.id, self.word, self.date_of_add, self.definition)
        return string_representation

    def display_translations(self):
        pass

class WordEng(Word):
    #TODO word_type do Word
    word_type = models.CharField(max_length=30, choices=wordDefinitions.ENG_WORD_TYPES, help_text='Select type of word', blank=True)

    def __str__(self):
        return "English Word: " + self.word + " " + self.word_type

    def display_word_type(self):
        """Create a string for the translation. This is required to display word_type in Admin."""
        return '{}'.format(self.word_type)

    def display_polword(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordpol_set.all())

    def display_translations(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordpol_set.all())

    display_polword.short_description = 'Polish Word'

    def __str__(self):
        string_representation = super(WordEng, self).__str__() + " {} ".format(self.word_type)
        return string_representation

    #TODO next by date
    def Next(self):
        try:
            # return WordEng.objects.get(pk=self.pk+1)
            next_issue = WordEng.objects.filter(date_of_add__gt=self.date_of_add).order_by('date_of_add').first()
            return next_issue
        except:
            return None

    def Previous(self):
        try:
            # return WordEng.objects.get(pk=self.pk-1)
            prev_issue = WordEng.objects.filter(date_of_add__lt=self.date_of_add).order_by('date_of_add').first()
            return prev_issue
        except:
            return None


class WordPol(Word):

    wordsEng = models.ManyToManyField(WordEng)
    word_type = models.CharField(max_length=30, choices=wordDefinitions.POL_WORD_TYPES, help_text='Select type of word', blank=True)

    def display_word_type(self):
        """Create a string for the translation. This is required to display word_type in Admin."""
        return '{}'.format(self.word_type)

    def display_engword(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordsEng.all())

    def display_translations(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordsEng.all())

    display_engword.short_description = 'English Word'

    def __str__(self):
        string_representation = super(WordPol, self).__str__() + " {} ".format(self.word_type)
        return string_representation

    def Next(self):
        try:
            # return WordEng.objects.get(pk=self.pk+1)
            next_issue = WordPol.objects.filter(pk__gt=self.pk).order_by('pk').first()
            return next_issue
        except:
            return None

    def Previous(self):
        try:
            # return WordEng.objects.get(pk=self.pk-1)
            prev_issue = WordPol.objects.filter(pk__lt=self.pk).order_by('pk').first()
            return prev_issue
        except:
            return None