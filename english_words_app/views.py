from django.views.generic import TemplateView


class Words(TemplateView):
    template_name = "english_words_app/words_list.html"
