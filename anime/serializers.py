from rest_framework import serializers
from .models import Anime, Review, UserAnimeRelation
from rest_framework.serializers import ModelSerializer


class AnimeSerializer(ModelSerializer):
  reviews_count = serializers.SerializerMethodField()

  likes = serializers.IntegerField(read_only=True)

  class Meta:
    model = Anime
    fields = ['id', 'name', 'year', 'description', 'genre', 'reviews_count', 'likes']
    # exclude = ('creator', )

  def get_reviews_count(self, instance):
    return Review.objects.filter(anime=instance).count()


class ReviewSerializer(ModelSerializer):
  class Meta:
    model = Review
    fields = ('creator', 'anime', 'created', 'edited', 'title', 'text', 'rate')


class UserAnimeRelationSerializer(ModelSerializer):
  class Meta:
    model = UserAnimeRelation
    # fields = '__all__'
    fields = ('like', 'in_bookmarks', 'anime')
