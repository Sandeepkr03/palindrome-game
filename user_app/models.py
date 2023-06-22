# game/models.py

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.CharField(max_length=255)
    is_palindrome = models.BooleanField(default=False)
    completed  = models.BooleanField(default=False)
