from django.shortcuts import render
from django.http import HttpResponseRedirect
from wordslearn.models import WordEng, WordPol
from wordslearn.DataHelpers import WordsHelpers
from django.urls import reverse
from django.views import generic
import datetime
# Create your views here.


from wordslearn.forms import AddEnglishWordForm, AddPolishWordForm

words_in_database = WordsHelpers.getNumberOfWords()
words_add_last_week = WordsHelpers.getNumberOfWords(7)

def index(request):

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
	paginate_by = 10

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
	paginate_by = 10

	def get_queryset(self):
		return WordPol.objects.all()

	def get_context_data(self, *, object_list=None, **kwargs):
		# Call the base implementation first to get the context
		context = super(WordPolListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		return context

# def add_english_word(request):
# 	newEngWord = WordEng(word="", word_type='Other', date_of_add=datetime.datetime.now())
# 	if request.method =='POST':
# 		# Create a form instance and populate it with data from the request (binding)
# 		form = AddEnglishWordModelForm(request.POST)
#
# 		if form.is_valid():
# 			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
# 			return HttpResponseRedirect(reverse('all-borrowed'))
#
# 	else:
# 		# If this is a GET (or any other method) create the default form
# 		word = "New Word"
# 		form = AddEnglishWordModelForm(initial={'word': word})
#
# 	context = {
# 		'form':form,
# 		'newEngWord': newEngWord
# 	}
#
# 	return render(request, 'wordslearn/new_eng_word.html', context)

def add_english_word(request):

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

				# redirect to a new URL:
				return HttpResponseRedirect(reverse('wordslearn:englishwords'))

	# If this is a GET (or any other method) create the default form.
	else:
		# initial form creation request.
		form = AddEnglishWordForm()

	context = {
		'form' : form,
		'word_instance' : word_instance
	}

	return render(request, 'wordslearn/new_eng_word.html', context)

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
	print("get detail for {}".format(word_id))
	try:
		word = WordEng.objects.get(pk=word_id)
	except WordEng.DoesNotExist:
		print("WordEng does not exist")
		# raise Http404("Word does not exist")

	print("get detailes for word: {}".format(word))

	context = {'word': word}
	return render(request, 'wordslearn/detailed_view.html', context)

def detailed_word_pol(request, word_id):

	word = None
	try:
		word = WordPol.objects.get(pk=word_id)
	except WordEng.DoesNotExist:
		print("WordEng does not exist")

	context = {'word': word}
	return render(request, 'wordslearn/detailed_view.html', context)


