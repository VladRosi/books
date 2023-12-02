from urllib import request
from django.db.models import Avg, Case, Count, Max, Min, When
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from store.permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from django.shortcuts import render
from .serializers import BooksSerializer, UserBookRelationSerializer
from .models import Book, UserBookRelation
# from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BookViewSet(ModelViewSet):
  # queryset = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))))#.order_by('id')
  # queryset = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), rating=Avg('userbookrelation__rate')).order_by('id')
  queryset = Book.objects.all().annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate') \
        ).select_related('owner').prefetch_related('readers')

  serializer_class = BooksSerializer
  filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
  permission_classes = [IsOwnerOrStaffOrReadOnly]
  filterset_fields = ['price']
  search_fields = ['name', 'author_name']
  ordering_fields = ['author_name', 'price']
  ordering = 'name'

  def perform_create(self, serializer):
    serializer.validated_data['owner'] = self.request.user
    serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
  permission_classes = [IsAuthenticated]
  queryset = UserBookRelation.objects.all()
  serializer_class = UserBookRelationSerializer
  lookup_field = 'book'

  def get_object(self):
    obj, was_created  = \
      UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
    # print('\n=================')
    # print('Was created:', was_created)
    # print('=================')
    return obj


def auth(request):
  return render(request, 'oauth.html')
