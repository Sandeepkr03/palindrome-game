# game/models.py

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.CharField(max_length=255)
    is_palindrome = models.BooleanField(default=False)
