from django import forms
from django.forms import ModelForm
from wordslearn.models import WordEng
from wordslearn.models import WordPol
from wordslearn import wordDefinitions
from django.core.exceptions import ValidationError

class AddEnglishWordFormSimple(forms.Form):
    word = forms.CharField(max_length=200, label='Enter the english word', help_text='Enter the english word')
    # validation
    def clean_word(self):
        word = self.cleaned_data['word']
        if not word.isalpha():
            raise ValidationError('Wrong word format')
        return word

    # custom validation for form
    def clean(self):
        cleaned_data = super().clean()
        word = self.cleaned_data.get("word")
        if not word:
            raise ValidationError('Missing word - add new word')


class AddEnglishWordForm(forms.Form):
    word = forms.CharField(max_length=200, label='Enter the english word', help_text='Enter the english word')
    polish_word = forms.CharField(max_length=200, label='Enter the polish translation', help_text='Enter the polish translation')
    synonym = forms.CharField(max_length=200, required=False,  label='Enter the synonym of english word', help_text='Enter the synonym of english word')
    antonym = forms.CharField(max_length=200, required=False, label='Enter the antonym of english word', help_text='Enter the antonym of english word')
    translation = ""
    definition = forms.CharField(max_length=200, required=False, label='Enter the definition of english word', help_text='Enter the definition of english word')
    word_type = forms.ChoiceField(choices=wordDefinitions.ENG_WORD_TYPES, label="Select type", initial='', widget=forms.Select(), required=True)

    # custom validation for fields word
    def clean_word(self):
        word = self.cleaned_data['word']
        if not word.isalpha():
            raise ValidationError('Wrong word format')
        return word

    def clean_polish_word(self):
        word = self.cleaned_data['polish_word']
        if not word.isalpha():
            raise ValidationError('Wrong word format')
        return word

    # custom validation for form
    def clean(self):
        cleaned_data = super().clean()
        word_eng = cleaned_data.get("word")
        word_pl = cleaned_data.get('polish_word')
        if not word_eng:
            raise ValidationError('Missing english words - add new word')

        if not word_pl:
            raise ValidationError('Missing polish word - add new word')


class AddPolishWordForm(forms.Form):
    word = forms.CharField(max_length=200, help_text='Enter the polish word')
    english_word = forms.CharField(max_length=200, help_text='Enter the english translation')

    word_type = forms.ChoiceField(choices=wordDefinitions.POL_WORD_TYPES, label="select type", initial='', widget=forms.Select(), required=True)

    # validation
    def clean_word(self):
        data = self.cleaned_data['word']
        if not data:
            raise ValidationError('Invalid word - add new word')

        return data

