from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, FormView

from .forms import CustomUserCreationForm
from .models import Word, Profile
from .tools import shred

@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def words_api(request: HttpRequest):
    user_id = request.GET.get("user_id")
    word_id = request.GET.get("word_id")
    profile = Profile.objects.get(user=User.objects.get(pk=int(user_id)))
    if not user_id or not word_id:
        return JsonResponse({"error": "bad request"}, status=400)
    if request.method == "DELETE":
        try:
            profile.favorites.remove(Word.objects.get(pk=int(word_id)))
        except (KeyError, Exception):
            return JsonResponse({"error": "bad request"}, status=400)
    else:
        try:
            profile.favorites.add(Word.objects.get(pk=int(word_id)))
        except (KeyError, Exception):
            return JsonResponse({"error": "bad request"}, status=400)
    return JsonResponse({"status": "ok"}, status=200)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("english_words_app:index")


class CustomLogoutView(LogoutView):
    template_name = "registration/logout.html"

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("english_words_app:index")


class Index(TemplateView):
    template_name = "english_words_app/index.html"

    def get_context_data(self, **kwargs):
        self.request.session["pages"] = None
        context = super().get_context_data(**kwargs)
        context["auth"] = self.request.user.is_authenticated
        return context

class Words(LoginRequiredMixin, ListView):
    _data_per_page = 10

    def get_queryset(self):
        if self.request.GET.get("next"):
            try:
                current_page = int(self.kwargs["page"]) + int(self.request.GET.get("next"))
            except TypeError as e:
                print(e)
                current_page = 0
        else:
            current_page = int(self.kwargs["page"])

        profile = Profile.objects.get(user=self.request.user)

        pages = self.request.session.get("pages")
        is_favorite = self.request.path.startswith("/favorite")
        if pages is None:
            if is_favorite:
                words = profile.favorites.order_by("?").values_list("pk", flat=True)
            else:
                words = Word.objects.order_by("?").values_list("pk", flat=True)
            pages = shred(self._data_per_page, words)
            self.request.session["pages"] = pages

        ids = pages[current_page % len(pages)]

        self.extra_context = {
            "is_favorite": is_favorite,
            "is_paginated": len(pages) > 1,
            "page": current_page,
            "favorites": [favorite.pk for favorite in profile.favorites.all()],
            "user": self.request.user
        }
        if is_favorite:
            return profile.favorites.filter(pk__in=ids)
        else:
            return Word.objects.filter(pk__in=ids)


class Register(FormView):
    form_class = CustomUserCreationForm
    template_name = "english_words_app/register.html"
    success_url = reverse_lazy("english_words_app:index")

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return super().form_valid(form)
