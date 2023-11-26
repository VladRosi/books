from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
  def setUp(self):
    self.book_1 = Book.objects.create(name="Book_1", price=14.50, author_name='Author 1')
    self.book_2 = Book.objects.create(name="Book_2", price=14.50, author_name='Author 1')
    self.book_3 = Book.objects.create(name="Book_3", price=25.70, author_name='Author 2')
    self.book_4 = Book.objects.create(name="Book_4", price=30.80, author_name='Author 2')
    self.book_5 = Book.objects.create(name="Book_5 about Author 1", price=35.90, author_name='Author 3')

  def test_get(self):
    url = reverse('book-list')
    response = self.client.get(url, data={'price': '14.50'})
    serializer_data = BooksSerializer([self.book_1, self.book_2], many=True).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(BooksSerializer(self.book_1).data, response.data[0])

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(200, response.status_code)

  def test_filter(self):
    url = reverse('book-list')
    response = self.client.get(url, data={'search': 'Author 1'})
    serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_5], many=True).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(BooksSerializer(self.book_1).data, response.data[0])

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(200, response.status_code)

  def test_sorting(self):
    url = reverse('book-list')
    response = self.client.get(url, data={'ordering': '-price'})
    serializer_data = BooksSerializer([self.book_5, self.book_4, self.book_3, self.book_4, self.book_1], many=True).data
    self.assertEqual(serializer_data[0], response.data[0])

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(200, response.status_code)
