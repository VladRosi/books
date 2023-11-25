from .models import Anime
from rest_framework.serializers import ModelSerializer


class AnimeSerializer(ModelSerializer):
  class Meta:
    model = Anime
    fields = "__all__"
