from django import forms
from django.forms import ModelForm
from wordslearn.models import WordEng
from wordslearn.models import WordPol

WORD_TYPES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
        ('other', 'Other')]

class AddEnglishWordForm(forms.Form):
    word = forms.CharField(max_length=200, help_text='Enter the english word')
    polish_word = forms.CharField(max_length=200, help_text='Enter the polish translation')

    word_type = forms.ChoiceField(choices=WORD_TYPES, label="select type", initial='', widget=forms.Select(), required=True)

    # validation
    def clean_word(self):
        data = self.cleaned_data['word']
        if not data:
            raise ValidationError('Invalid word - add new word')

        return data

#
# class AddEnglishWordModelForm(ModelForm):
#     class Meta:
#         model = WordEng
#         fields = ['word']
#         # labels = {'wordpol_set': ('Add Polish translation')}
#
#     polwords = forms.ModelMultipleChoiceField(queryset=WordPol.objects.all())
#
#     def __init__(self, *args, **kwargs):
#         if kwargs.get('instance'):
#             initial = kwargs.setdefault('initial', {})
#             initial['wordpol'] = [t.pk for w in kwargs['instance']].wordpol_set.all()
#         forms.ModelForm.__init__(self, *args, **kwargs)
#
#     def save(self):
#         # Get the unsave english word instance
#         instance = forms.ModelForm.save(self, False)
#
#         # Prepare a 'save_m2m' method for the form
#         old_save_m2m = self.save_m2m
#         def save_m2m():
#             old_save_m2m()
#             # This is where we actually link the english word with polish words
#             instance.polword_set.clear()
#             instance.polword_set.add(*self.cleaned_data['polwords'])
#         self.save_m2m = save_m2m
#
#         if commit:
#             instance.save()
#             self.save_m2m()
#
#         return instance
#
#     #validation for date_of_add field
#     def clean_date_of_add(self):
#         data = self.cleaned_data['date_of_add']
#
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - adding in past'))
#
#         return data