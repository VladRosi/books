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
  reviews = models.ManyToManyField(to=User, through='Review', related_name='reviews')
  watchers = models.ManyToManyField(User, through='UserAnimeRelation', related_name='watchers')

  def __str__(self):
    return self.name


class Review(models.Model):
  RATE_CHOICES = (
    (1, "It couldn't be worse!"),
    (2, 'Horrible'),
    (3, 'Very bad'),
    (4, 'Bad but not very'),
    (5, 'Ok'),
    (6, 'Nice, but could be better'),
    (7, 'Good'),
    (8, 'Very good'),
    (9, 'Incredible'),
    (10, 'Divine'),
  )
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
  created = models.DateTimeField(null=True)
  edited = models.DateTimeField(null=True)
  title = models.CharField(max_length=255, default='')
  text = models.TextField(default='')
  rate = models.SmallIntegerField(choices=RATE_CHOICES, default=5)

  def __str__(self):
    title_l = self.title.split(" ")
    anime_l = self.anime.name.split(" ")
    title = ' '.join(title_l) if len(title_l) <= 5 else ' '.join(title_l[:5]) + '..'
    anime_name = ' '.join(anime_l) if len(anime_l) <= 5 else ' '.join(anime_l[:5]) + '..'
    return f'Title: “{title}”, Creator: “{self.creator.username}”, Anime: “{anime_name}”.'


class UserAnimeRelation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
  like = models.BooleanField(default=False)
  in_bookmarks = models.BooleanField(default=False)

  def __str__(self):
    return f"User: “{self.user.username}”, Anime: “{self.anime.name}”."
