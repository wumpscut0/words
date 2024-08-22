from django.urls import path

from .views import Words, Index, Register, CustomLoginView, CustomLogoutView, words_api

app_name = "english_words_app"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("dictionary/<slug:page>", Words.as_view(), name="word_list"),
    path("favorite/<slug:page>", Words.as_view(), name="favorite_list"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("api/v1/words/delete", words_api),
    path("api/v1/words/add", words_api),
]