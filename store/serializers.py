from cryptography.hazmat.primitives import serialization
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.representation import serializer_repr
from .models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
  # likes_count = serializers.SerializerMethodField()
  # list_of_users = serializers.SerializerMethodField()
  # final_price = serializers.SerializerMethodField()
  annotated_likes = serializers.IntegerField(read_only=True)  # note: Appending some field to each element of output out query
  rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)  # note: Don't forget to add 'read_only=True'
  max_rating = serializers.IntegerField(read_only=True)
  min_rating = serializers.IntegerField(read_only=True)
  owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
  owner_name = serializers.CharField(read_only=True) # exe
  
  

  # readers_abs = BookReaderSerializer(many=True, source='readers')
  readers = BookReaderSerializer(many=True, read_only=True)

  class Meta:
    model = Book
    fields = ['id', 'name', 'price', 'author_name', 'annotated_likes', 'rating', 'discount', 'max_rating', 'min_rating', 'owner_name', 'readers']

  # def get_likes_count(self, instance):
  #   return UserBookRelation.objects.filter(book=instance, like=True).count()

  # def get_list_of_users(self, instance):
  #   return len(list(map(lambda relation: relation.user.username, UserBookRelation.objects.filter(book=instance, in_bookmarks=True))))

  # def get_final_price(self, instance):
  #   price = float(instance.price)
  #   discount = float(instance.discount)

  # return '{:0.2f}'.format(round(price - price * (discount / 100), 2))


class UserBookRelationSerializer(ModelSerializer):
  class Meta:
    model = UserBookRelation
    exclude = ('user', )
