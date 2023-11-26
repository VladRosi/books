from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Anime
from .serializers import AnimeSerializer
from rest_framework.viewsets import ModelViewSet


class AnimeViewSet(ModelViewSet):
  queryset = Anime.objects.all()
  serializer_class = AnimeSerializer
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_fields = ['year']
  search_fields = ['name', 'genre']
  ordering_fields = ['year', 'genre', 'name']
  ordering = 'year'
