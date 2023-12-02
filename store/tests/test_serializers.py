from django.contrib.auth.models import User
from django.db.models import Q, Avg, Case, Count, Exists, Value, When, Max, Min, Aggregate
from django.db.models.expressions import BaseExpression
from django.test import TestCase
from nine import user
from sqlparse.sql import Where
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
  def test_ok(self):
    user_1 = User.objects.create(username='user_1', password='test_password', first_name='first', last_name='last')
    user_2 = User.objects.create(username='user_2', password='test_password')
    user_3 = User.objects.create(username='user_3', password='test_password')

    book_1 = Book.objects.create(owner=user_1, name="Advanced Japanese", price=19.90, author_name='Author 1', discount=15)
    book_2 = Book.objects.create(owner=user_2, name="Advanced English", price=15.45, author_name='Author 1')
    book_3 = Book.objects.create(name="I and my ass", price=19, author_name='Author 2')

    UserBookRelation.objects.create(user=user_1, book=book_1, like=True, in_bookmarks=False)
    UserBookRelation.objects.create(user=user_1, book=book_2, like=True, in_bookmarks=True, rate=3)
    UserBookRelation.objects.create(user=user_1, book=book_3, like=True, in_bookmarks=False, rate=3)

    UserBookRelation.objects.create(user=user_2, book=book_1, like=True, in_bookmarks=True)
    UserBookRelation.objects.create(user=user_2, book=book_2, like=False, in_bookmarks=True, rate=2)
    UserBookRelation.objects.create(user=user_2, book=book_3, like=True, in_bookmarks=True, rate=3)

    user3_book1 = UserBookRelation.objects.create(user=user_3, book=book_1, in_bookmarks=False)
    user3_book1.rate = 3
    user3_book1.save()
    
    
    UserBookRelation.objects.create(user=user_3, book=book_2, in_bookmarks=False, rate=2)
    UserBookRelation.objects.create(user=user_3, book=book_3, like=True, in_bookmarks=True)

    books = Book.objects.all().annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate'), \
        ).order_by('id')

    data = BooksSerializer(books, many=True).data

    print('-------------------')
    for d in data:
      print(d['owner_name'])
    print('-------------------')
    expected_data = [
      {
        'id': book_1.id,
        'name': 'Advanced Japanese',
        'price': '19.90',
        'author_name': 'Author 1',
        # 'likes_count': 2,
        'annotated_likes': 2,
        # 'list_of_users': 1,
        'rating': '3.00',
        'discount': '15.00',
        'max_rating': 3,
        'min_rating': 3,
        'owner_name': 'user_1',
        'readers': [
          {
            'first_name': 'first',
            'last_name': 'last'
          },
          {
            'first_name': '',
            'last_name': ''
          },
          {
            'first_name': '',
            'last_name': ''
          },
        ]
        # 'final_price': '16.91'
      },
      {
        'id': book_2.id,
        'name': 'Advanced English',
        'price': '15.45',
        'author_name': 'Author 1',
        # 'likes_count': 1,
        'annotated_likes': 1,
        # 'list_of_users': 2,
        'rating': '2.33',
        'discount': '0.00',
        'max_rating': 3,
        'min_rating': 2,
        'owner_name': 'user_2',
        'readers': [
          {
            'first_name': 'first',
            'last_name': 'last'
          },
          {
            'first_name': '',
            'last_name': ''
          },
          {
            'first_name': '',
            'last_name': ''
          },
        ]
        # 'final_price': '15.45'
      },
      {
        'id': book_3.id,
        'name': 'I and my ass',
        'price': '19.00',
        'author_name': 'Author 2',
        # 'likes_count': 3,
        'annotated_likes': 3,
        # 'list_of_users': 2,
        'rating': '3.00',
        'discount': '0.00',
        'max_rating': 3,
        'min_rating': 3,
        'owner_name': '',
        'readers': [
          {
            'first_name': 'first',
            'last_name': 'last'
          },
          {
            'first_name': '',
            'last_name': ''
          },
          {
            'first_name': '',
            'last_name': ''
          },
        ]
        # 'final_price': '19.00', # exe
      },
    ]
    print('========================================')
    for i in data:
      print('-----------')
      print(i)
      print('-----------')
    print('========================================')
    self.assertEquals(expected_data, data)
