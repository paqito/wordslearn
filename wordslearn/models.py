from django.db import models
from wordslearn import wordDefinitions

# Create your models here.
class Word(models.Model):

    word = models.CharField(max_length=200, help_text='Enter the word')
    date_of_add = models.DateTimeField(auto_now=True, blank=True, help_text='date added')

    class Meta:
        abstract = True
        ordering = ["word"]
    def __str__(self):
        return self.word

class WordEng(Word):

    word_type = models.CharField(max_length=30, choices=wordDefinitions.ENG_WORD_TYPES, help_text='Select type of word')

    def __str__(self):
        return "English Word: " + self.word + " " + self.word_type

    def display_polword(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordpol_set.all())

    display_polword.short_description = 'Polish Word'


    # def add_polish_word(self, pol_word):
    #     if pol_word not in self.wordpol_set.all():
    #         #create polish word
    #         newWord = WordPol(word=pol_word)
    #     else:
    #         #get exisitng word


class WordPol(Word):

    wordsEng = models.ManyToManyField(WordEng)
    word_type = models.CharField(max_length=30, choices=wordDefinitions.POL_WORD_TYPES, help_text='Select type of word')

    def __str__(self):
        return "Polish  Word: " + self.word + " " + self.word_type

    def display_engword(self):
        """Create a string for the translation. This is required to display WordEng in Admin."""
        return ', '.join(str(w.word) for w in self.wordsEng.all())

    display_engword.short_description = 'English Word'