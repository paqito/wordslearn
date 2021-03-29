from django.contrib import admin
from django import forms
from .models import WordEng
from .models import WordPol


class WordEngAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word', 'word_type', 'display_polword', 'date_of_add', 'definition', 'synonym', 'antonym')

class WordPolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word', 'word_type', 'display_engword', 'date_of_add', 'definition', 'synonym', 'antonym')

# Register your models here.
admin.site.register(WordEng, WordEngAdmin)
admin.site.register(WordPol, WordPolAdmin)