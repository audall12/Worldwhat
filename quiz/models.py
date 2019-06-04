from django.db import models


class HighScore(models.Model):
    score = models.IntegerField()
    name = models.CharField(max_length=8)

    def __int__(self):
        return self.score

    def __str__(self):
        return str(self.score) + ' ' + self.name


class Average(models.Model):
    score = models.IntegerField()
    games = models.IntegerField()

    def __int__(self):
        return self.score

    def __str__(self):
        return str(self.score)

