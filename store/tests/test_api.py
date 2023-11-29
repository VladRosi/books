import json
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username='test_name', password='test_password')
    self.user_2 = User.objects.create(username='test_name_2', password='test_password')
    self.staff_user = User.objects.create(username='staff_user', password='test_password', is_staff=True)

    self.book_1 = Book.objects.create(name="Book_1", price=14.50, author_name='Author 1', owner=self.user)
    self.book_2 = Book.objects.create(name="Book_2", price=14.50, author_name='Author 1', owner=self.user)
    self.book_3 = Book.objects.create(name="Book_3", price=25.70, author_name='Author 2', owner=self.user)
    self.book_4 = Book.objects.create(name="Book_4", price=30.80, author_name='Author 2', owner=self.user)
    self.book_5 = Book.objects.create(name="Book_5 about Author 1", price=35.90, author_name='Author 3', owner=self.user)
    self.url = reverse('book-list')

  def test_get_all(self):
    response = self.client.get(self.url, data={'price': '14.50'})
    serializer_data = BooksSerializer([self.book_1, self.book_2], many=True).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(BooksSerializer(self.book_1).data, response.data[0])
    self.assertEquals(status.HTTP_200_OK, response.status_code)

  def test_get_one(self):
    detail_url = reverse('book-detail', args=(self.book_1.id, ))
    response = self.client.get(detail_url)
    serializer_data = BooksSerializer(self.book_1).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(status.HTTP_200_OK, response.status_code)

  def test_filter(self):
    response = self.client.get(self.url, data={'search': 'Author 1'})
    serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_5], many=True).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(BooksSerializer(self.book_1).data, response.data[0])
    self.assertEquals(status.HTTP_200_OK, response.status_code)

  def test_sorting(self):

    response = self.client.get(self.url, data={'ordering': '-price'})
    serializer_data = BooksSerializer([self.book_5, self.book_4, self.book_3, self.book_4, self.book_1], many=True).data
    self.assertEqual(serializer_data[0], response.data[0])
    self.assertEquals(status.HTTP_200_OK, response.status_code)

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
