import json
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Avg, Case, Count, Max, Min, When
from django.test.utils import CaptureQueriesContext
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username='test_name', password='test_password')
    self.user_2 = User.objects.create(username='test_name_2', password='test_password')
    self.staff_user = User.objects.create(username='staff_user', password='test_password', is_staff=True)

    self.book_1 = Book.objects.create(name="Book_1", price=14.50, author_name='Author 1', owner=self.user, discount=10)
    self.book_2 = Book.objects.create(name="Book_2", price=14.50, author_name='Author 1', owner=self.user)
    self.book_3 = Book.objects.create(name="Book_3", price=25.70, author_name='Author 2', owner=self.user)
    self.book_4 = Book.objects.create(name="Book_4", price=30.80, author_name='Author 2', owner=self.user)
    self.book_5 = Book.objects.create(name="Book_5 about Author 1", price=35.90, author_name='Author 3', owner=self.user)

    UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, in_bookmarks=False, rate=5)
    UserBookRelation.objects.create(user=self.user_2, book=self.book_1, like=True, in_bookmarks=True, rate=3)

    self.url = reverse('book-list')

  def test_get_all(self):

    with CaptureQueriesContext(connection) as queries:
      response = self.client.get(self.url, data={'price': '14.50'})
      self.assertEqual(2, len(queries))
      


    books = Book.objects.filter(price='14.50') \
      .annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate') \
        ).order_by('id')

    serializer_data = BooksSerializer(books, many=True).data
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEqual(serializer_data, response.data)

  def test_get_one(self):
    detail_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.get(detail_url)

    book = Book.objects.filter(id__in=[self.book_1.id])  \
      .annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate') \
        ).order_by('id')

    serializer_data = BooksSerializer(book, many=True).data
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEqual(serializer_data[0], response.data)
    self.assertEqual(serializer_data[0]['rating'], '4.00')
    # self.assertEqual(serializer_data[0]['likes_count'], 2)
    self.assertEqual(serializer_data[0]['annotated_likes'], 2)
    self.assertEqual(serializer_data[0]['min_rating'], 3)
    self.assertEqual(serializer_data[0]['max_rating'], 5)
    # self.assertEqual(serializer_data[0]['final_price'], '13.05')

  def test_get_search(self):
    books = Book.objects.filter(id__in=[self.book_1.id, self.book_2.id, self.book_5.id]) \
      .annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate') \
        ).order_by('id')
    serializer_data = BooksSerializer(books, many=True).data
    response = self.client.get(self.url, data={'search': 'Author 1'})
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEqual(serializer_data, response.data)

  def test_sorting(self):
    response = self.client.get(self.url, data={'ordering': 'price'})
    books = Book.objects.all() \
      .annotate( \
      annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), \
      # rating=Avg('userbookrelation__rate'), \
      max_rating=Max('userbookrelation__rate'), \
      min_rating=Min('userbookrelation__rate') \
        ).select_related('owner').prefetch_related('readers').order_by('price')

    serializer_data = BooksSerializer(books, many=True).data
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEqual(serializer_data[0], response.data[0])

  def test_create(self):
    self.assertEqual(5, Book.objects.all().count())
    data = {"name": "My Fucking Life", "price": 39.99, "author_name": "Vlad Rosi"}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    response = self.client.post(self.url, data=json_data, content_type='application/json')
    self.assertEquals(status.HTTP_201_CREATED, response.status_code)
    self.assertEqual(6, Book.objects.all().count())
    self.assertEqual(self.user, Book.objects.last().owner)

  def test_update(self):
    data = {"name": self.book_1.name, "price": 227.99, "author_name": self.book_1.author_name}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    book1_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.put(book1_url, data=json_data, content_type='application/json')
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    # self.book_1 = Book.objects.get(id=self.book_1.id)
    self.book_1.refresh_from_db()
    self.assertEqual('227.99', str(self.book_1.price))

  def test_update_not_owner(self):
    data = {"name": self.book_1.name, "price": 227.99, "author_name": self.book_1.author_name}
    json_data = json.dumps(data)
    self.client.force_login(self.user_2)
    book1_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.put(book1_url, data=json_data, content_type='application/json')
    self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)
    # self.book_1 = Book.objects.get(id=self.book_1.id)
    self.book_1.refresh_from_db()
    self.assertEqual('14.50', str(self.book_1.price))
    self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}, response.data)

  def test_update_not_owner_but_staff(self):
    data = {"name": self.book_1.name, "price": 227.99, "author_name": self.book_1.author_name}
    json_data = json.dumps(data)
    self.client.force_login(self.staff_user)
    book1_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.put(book1_url, data=json_data, content_type='application/json')
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    # self.book_1 = Book.objects.get(id=self.book_1.id)
    self.book_1.refresh_from_db()
    self.assertEqual('227.99', str(self.book_1.price))

  def test_delete(self):
    self.assertEqual(Book.objects.all().count(), 5)
    self.client.force_login(self.user)
    book1_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.delete(book1_url, content_type='application/json')
    self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
    self.assertEqual(Book.objects.all().count(), 4)

  def test_delete_not_owner(self):
    self.assertEqual(Book.objects.all().count(), 5)
    self.client.force_login(self.user_2)
    book1_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.delete(book1_url, content_type='application/json')
    self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)
    self.assertEqual(Book.objects.all().count(), 5)


class BooksRelationApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username='test_name', password='test_password')
    self.user_2 = User.objects.create(username='test_name_2', password='test_password')
    self.staff_user = User.objects.create(username='staff_user', password='test_password', is_staff=True)

    self.book_1 = Book.objects.create(name="Book_1", price=14.50, author_name='Author 1', owner=self.user)
    self.book_2 = Book.objects.create(name="Book_2", price=34.50, author_name='Author 2', owner=self.user)
    self.url = reverse('userbookrelation-detail', args=(self.book_1.id, ))

  def test_have_like(self):
    data = {"like": True}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    # self.book_1.refresh_from_db()
    relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
    self.assertTrue(relation.like)

    data = {'in_bookmarks': True}
    json_data = json.dumps(data)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertTrue(relation.in_bookmarks)

  def test_rate(self):
    data = {'rate': 3}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    # self.book_1.refresh_from_db()
    relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
    self.assertEqual(3, relation.rate)

  def test_rate_wrong(self):
    data = {'rate': 9}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code, '\n' + str(resp.data) + '\n')
    # self.book_1.refresh_from_db()
    # relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
    # self.assertEqual(3, relation.rate)

  # def test_likes_count(self):
  #   self.client.force_login(self.user)
  #   resp = self.client.get(self.)
