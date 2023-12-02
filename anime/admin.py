from django.contrib import admin
from .models import Anime, Review, UserAnimeRelation


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
  pass


@admin.register(Review)
class AnimeAdmin(admin.ModelAdmin):
  pass


@admin.register(UserAnimeRelation)
class AnimeAdmin(admin.ModelAdmin):
  pass
