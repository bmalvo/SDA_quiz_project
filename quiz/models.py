from django.db import models


class Quiz(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    difficult = models.CharField(
        choices=Difficulty.choices
    )

    number_of_questions = models.IntegerField()

