from django.urls import path

from . import views
app_name = 'wordslearn'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('<int:word_id>/', views.detail, name="detail"),
    path('englishwords/', views.WordEngListView.as_view(), name='englishwords'),
    path('polishwords/', views.WordPolListView.as_view(), name='polishwords'),
    path('addsimpleenglishword/', views.add_english_word_simple, name="add-english-word-simple"),
    path('addenglishword/', views.add_english_word, name="add-english-word"),
    path('addpolishhword/', views.add_polish_word, name="add-polish-word")
]