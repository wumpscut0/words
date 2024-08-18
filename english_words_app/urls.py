from django.urls import path
from english_words_app.views import Words


app_name = "english_words_app"

urlpatterns = [
    path("", Words.as_view(), name="word_list")
]