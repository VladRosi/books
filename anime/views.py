from .models import Anime
from .serializers import AnimeSerializer
from rest_framework.viewsets import ModelViewSet


class AnimeViewSet(ModelViewSet):
  queryset = Anime.objects.all()
  serializer_class = AnimeSerializer
