from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    en = models.CharField(max_length=30)
    ru = models.JSONField(default=list, null=True)
    transcription = models.CharField(max_length=30, null=True, blank=True)
    data = models.JSONField(default=dict, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Word, related_name="favorites")
