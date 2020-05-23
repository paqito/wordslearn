from django import forms
from django.forms import ModelForm
from wordslearn.models import WordEng
from wordslearn.models import WordPol
from wordslearn import wordDefinitions


class AddEnglishWordForm(forms.Form):
    word = forms.CharField(max_length=200, help_text='Enter the english word')
    polish_word = forms.CharField(max_length=200, help_text='Enter the polish translation')

    word_type = forms.ChoiceField(choices=wordDefinitions.ENG_WORD_TYPES, label="select type", initial='', widget=forms.Select(), required=True)

    # validation
    def clean_word(self):
        data = self.cleaned_data['word']
        if not data:
            raise ValidationError('Invalid word - add new word')

        return data


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

