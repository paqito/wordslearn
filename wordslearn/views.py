from django.shortcuts import render
from django.http import HttpResponseRedirect
from wordslearn.models import WordEng, WordPol
from django.urls import reverse
from django.views import generic
import datetime
# Create your views here.


from wordslearn.forms import AddEnglishWordForm

def index(request):
	return render(request, 'index.html')

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