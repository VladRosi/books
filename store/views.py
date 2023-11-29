from django.shortcuts import render
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from store.permissions import IsOwnerOrStaffOrReadOnly
from .models import Book
from .serializers import BooksSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(ModelViewSet):
  queryset = Book.objects.all()
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


def auth(request):
  return render(request, 'oauth.html')
