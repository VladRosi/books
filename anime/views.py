from django.db.models import Count, Case, When
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from anime.permissions import IsCreatorOrStaffOrReadOnly
from .models import Anime, Review, UserAnimeRelation
from .serializers import AnimeSerializer, ReviewSerializer, UserAnimeRelationSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class AnimeViewSet(ModelViewSet):
  queryset = Anime.objects.all().annotate(likes=Count(Case(When(useranimerelation__like=True, then=1))))
  serializer_class = AnimeSerializer
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  permission_classes = [IsCreatorOrStaffOrReadOnly]
  filterset_fields = ['year']
  search_fields = ['name', 'genre']
  ordering_fields = ['year', 'genre', 'name']
  ordering = 'year'


class UserAnimeRelationView(UpdateModelMixin, GenericViewSet):
  permission_classes = [IsAuthenticated]
  queryset = UserAnimeRelation.objects.all()
  serializer_class = UserAnimeRelationSerializer
  lookup_field = 'anime'
  def get_object(self):
    obj, _ = UserAnimeRelation.objects.get_or_create(user=self.request.user, anime_id=self.kwargs['anime'])
    return obj


class ReviewView(UpdateModelMixin, GenericViewSet):
  permission_classes = [IsAuthenticated]
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer
  lookup_field = 'anime'

  def get_object(self):
    obj, _ = Review.objects.get_or_create(creator=self.request.user, anime_id=self.kwargs['anime'])
    return obj
