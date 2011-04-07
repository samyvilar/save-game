from django.db import models
from django.contrib.auth.models import User

max_length = 512

PLATFORM_CHOICES = (
        ("PlayStation 3", "PlayStation 3"),
        ("PlayStation 2", "PlayStation 2"),
        ("PlayStation 1", "PlayStation 1"),
        ("Xbox", "Xbox"),
        ("Xbox 360", "Xbox 360"),
        ("Wii", "Wii"),
        ("GameCube", "GameCube"),
        ("Nintendo 64", "Nintendo 64")
    )

class Game(models.Model):
    title    = models.CharField("Title", max_length = max_length)
    year     = models.IntegerField("Year")
    company  = models.CharField("Company", max_length = max_length)
    platform = models.CharField("Plaform", max_length = max_length, choices = PLATFORM_CHOICES)


class SavedGame(models.Model):
    file    = models.FileField(upload_to = "saved_games")
    date    = models.DateField("Date")
    game    = models.ForeignKey(Game, verbose_name = "Game")
    user    = models.ForeignKey(User, verbose_name = "User")
    private = models.BooleanField("Private")

class Comment(models.Model):
    title       = models.CharField("Title", max_length = max_length)
    body        = models.TextField("Body", max_length = max_length)
    date        = models.DateField("Date")
    game        = models.ForeignKey(Game, verbose_name = "Game")
    savedgame   = models.ForeignKey(SavedGame)
    user        = models.ForeignKey(User)

