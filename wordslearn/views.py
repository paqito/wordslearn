from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from wordslearn.models import WordEng, WordPol, create_eng_word, create_pol_word, LanguageChoice
from wordslearn.DataHelpers import WordsHelpers
from django.urls import reverse
from django.views import generic

# from wordsData.translatorModule import WordDetail
from utilities import translate_utility
import datetime
# Create your views here.

from wordslearn.forms import AddEnglishWordFormSimple
from wordslearn.forms import AddEnglishWordForm, AddPolishWordForm

words_in_database = WordsHelpers.getNumberOfWords()
words_add_last_week = WordsHelpers.getNumberOfWords(7)

def index(request):
	'''
	Render main page with default informatino about the words in the db
	:param request:
	:return:
	'''

	# get 5 last eng and pol words
	end_words = WordsHelpers.getLatestWord()
	# end_words = WordEng.objects.order_by('-date_of_add')[:5]
	pol_words = WordPol.objects.order_by('-date_of_add')[:5]

	timedelta_words = WordsHelpers.getNumberOfWordsInDataRange()

	context = {	'words_in_database' : words_in_database,
				'words_add_last_week' : words_add_last_week,
				'latest_eng_words': end_words,
			   	'latest_pol_words': pol_words,
			   	'timedelta_words' : timedelta_words}

	return render(request, 'index.html', context)

class WordEngListView(generic.ListView):
	model = WordEng
	paginate_by = 20

	def get_queryset(self):
		return WordEng.objects.all()

	def get_context_data(self, *, object_list=None, **kwargs):
		# Call the base implementation first to get the context
		context = super(WordEngListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		return context

class WordPolListView(generic.ListView):
	model = WordPol
	paginate_by = 20

	def get_queryset(self):
		return WordPol.objects.all()

	def get_context_data(self, *, object_list=None, **kwargs):
		# Call the base implementation first to get the context
		context = super(WordPolListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		return context

def add_english_word_simple(request):
	'''
	Function to create Word Model instance based on translation
	:param request: Word from AddEnglishWordFormSimple
	:return:
	'''
	print("add_english_word_simple method : {}".format(request.method))

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = AddEnglishWordFormSimple(request.POST)
		# check whether it's valid:
		if form.is_valid():
			word = form.cleaned_data['word']
			# type = form.cleaned_data['word']
			# process the data in form.cleaned_data as required
			print("[views.py] add_english_word_simple {}".format(word))

			# check if word to translate already exists in db
			#TODO add every word
			exists = True
			if exists:
				print("[views.py] Adding new word in database {}".format(word))
				# add new world

				# try to translate word, returns list of WordDetail
				# translations - list of WordDetails
				translations = translate_utility.translate_words(word)
				print("[views.py] translations number {}: {}".format(len(translations), str(translations)))

				# if any(w.translation !="" for w in translations):
				if any(w.word != "" for w in translations):
					for word_details in translations:
						print("[views.py] word_details {}".format(word_details))
						if word_details.word != "":
							# TODO create the word
							'''
							class WordDetail:
								word = ""
								synonym = ""
								antonym = ""
								type = ""
								translation = ""
								definition = ""
							'''
							# converting wordDetails into Word Model
							kwarg = {"word" : word_details.word, "synonym" : word_details.synonym, "antonym": word_details.antonym,
									 "definition": word_details.definition, "translation": word_details.translation, "type":word_details.type }
							print(str(kwarg))

							# check if word to translate already exists in db
							# TODO add every word
							word_instance = WordsHelpers.getWordFromDb(word, LanguageChoice.EN, word_details.type)
							if word_instance is None:
								word_instance = create_eng_word(**kwarg)

							# check if polish_word already exists
							existing_polish_word = WordsHelpers.getWordFromDb(word_details.translation, LanguageChoice.PL, word_details.type)
							# existing_polish_word = WordPol.objects.filter(word__exact=word_details.translation)
							if existing_polish_word:
								# exists
								for word in existing_polish_word:
									# add m2m relation
									word_instance.wordpol_set.add(word)
									word_instance.save()

							else:
								# must add polish word
								if word_details.translation:
									kwarg = {"word": word_details.translation,  "type": word_details.type}
									polish_word_instance = create_pol_word(**kwarg)
									# polish_word_instance = WordPol(word=word_details.translation)
									# polish_word_instance.save()
									polish_word_instance.wordsEng.add(word_instance)
									polish_word_instance.save()

					# redirect to a new URL:
					return HttpResponseRedirect(reverse('wordslearn:englishwords'))

				else:
					print("[views.py] Redirect to add-english-word")
					# render more complex new word form
					initial_dict = {
						"word": word
					}
					form = AddEnglishWordForm(initial=initial_dict)
					form.word = word

					context = {'form': form}
					# return render(request, "wordslearn/new_eng_word.html", context)

					# return redirect('wordslearn:add-english-word')
					# return redirect(reverse('wordslearn:add-english-word'), context)
					return HttpResponseRedirect(reverse('wordslearn:add-english-word'), context)

			# else:
			# 	# words already exists
			# 	print("[views.py] World already exist: {} id: {}".format(exists.word, exists.pk))
			# 	# redirect to url with detailes of word
			#
			# 	context = {'word': exists}
			# 	return render(request, 'wordslearn/detailed_view.html', context)
			# 	# TODO redirect to ditailed view
			# 	# return HttpResponseRedirect(reverse('wordslearn:detail', args=[]))

	else:
		# if a GET (or any other method) we'll create a blank form
		form = AddEnglishWordFormSimple()

	context = {'form': form}
	return render(request, 'wordslearn/new_eng_word_simple.html', context)
	# return HttpResponseRedirect(reverse('wordslearn:englishwords'))


def add_english_word(request):

	print("[views.py] add_english_word method : {}".format(request.method))
	word_instance = WordEng()
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = AddEnglishWordForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			word_instance.word = form.cleaned_data['word']
			polish_word = form.cleaned_data['polish_word']
			word_instance.word_type = form.cleaned_data['word_type']
			word_instance.save()

			# check if polish_word already exists
			existing_polish_word = WordPol.objects.filter(word__exact=polish_word)
			if existing_polish_word:
				# exists
				for word in existing_polish_word:
					# add m2m relation
					word_instance.wordpol_set.add(word)
					word_instance.save()

			else:
				# must add polish word
				polish_word_instance = WordPol(word=polish_word)
				polish_word_instance.save()
				polish_word_instance.wordsEng.add(word_instance)
				polish_word_instance.save()

		print("[views.py] redirect to englishwords")
		# return render(request, 'wordslearn/new_eng_word_simple.html', context)
		# redirect to a new URL:
		return HttpResponseRedirect(reverse('wordslearn:englishwords'))

	# If this is a GET (or any other method) create the default form.
	else:
		# initial form creation request.
		form = AddEnglishWordForm()

	context = {
		'form':form,
		'word_instance':word_instance
	}

	return render(request, 'wordslearn/new_eng_word.html', context)
	# return HttpResponseRedirect(reverse('wordslearn:englishwords'))

def add_polish_word(request):

	word_instance = WordPol()
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = AddPolishWordForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			word_instance.word = form.cleaned_data['word']
			english_word = form.cleaned_data['english_word']
			word_instance.word_type = form.cleaned_data['word_type']
			word_instance.save()

			# check if english_word already exists
			existing_english_word = WordPol.objects.filter(word__exact=english_word)
			if existing_english_word:
				# exists
				for word in existing_english_word:
					# add m2m relation
					word_instance.wordsEng.add(word)
					word_instance.save()

			else:
				# must add english word
				english_word_instance = WordEng(word=english_word)
				english_word_instance.save()
				english_word_instance.wordpol_set.add(word_instance)
				english_word_instance.save()

				# redirect to a new URL:
				return HttpResponseRedirect(reverse('wordslearn:polishwords'))

	# If this is a GET (or any other method) create the default form.
	else:
		# initial form creation request.
		form = AddPolishWordForm()

	context = {
		'form' : form,
		'word_instance' : word_instance
	}

	return render(request, 'wordslearn/new_pol_word.html', context)

def detail(request, word_id):

	word = None
	print("[views.py] get detail for {}".format(word_id))
	try:
		word = WordEng.objects.get(pk=word_id)
	except WordEng.DoesNotExist:
		print("WordEng does not exist")
		# raise Http404("Word does not exist")
	if not word:
		try:
			word = WordPol.objects.get(pk=word_id)
		except WordPol.DoesNotExist:
			print("WordPol does not exist")
			# raise Http404("Word does not exist")

	print("get detailes for word: {}".format(word))

	context = {'word': word}
	return render(request, 'wordslearn/detailed_view.html', context)

def detailed_word_pol(request, word_id):

	word = None
	try:
		word = WordPol.objects.get(pk=word_id)
	except WordEng.DoesNotExist:
		print("[views.py] WordEng does not exist")

	context = {'word': word}
	return render(request, 'wordslearn/detailed_view.html', context)


