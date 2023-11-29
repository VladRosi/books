from django.contrib.auth.models import User
from django.db import models


class Anime(models.Model):
  THRILLER = 'TR'
  HORROR = 'HR'
  ROMANCE = 'RM'
  ADVENTURE = 'AD'
  ACTION = 'AC'

  GENRES_OF_ANIME = [
    (THRILLER, 'Thriller'),
    (HORROR, 'Horror'),
    (ROMANCE, 'Romance'),
    (ADVENTURE, 'Adventure'),
    (ACTION, 'Action'),
  ]

  name = models.CharField(max_length=255)
  year = models.IntegerField()
  description = models.TextField(blank=True)
  genre = models.CharField(choices=GENRES_OF_ANIME, max_length=2, default=ACTION)
  creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.name