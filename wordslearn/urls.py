from django.urls import path

from . import views
app_name = 'wordslearn'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('englishwords/', views.WordEngListView.as_view(), name='englishwords'),
    path('polishwords/', views.WordPolListView.as_view(), name='polishwords'),
    path('addenglishword/', views.add_english_word, name="add-english-word")
]