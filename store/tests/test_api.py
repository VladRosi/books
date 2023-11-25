from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
  def test_get(self):
    book_1 = Book.objects.create(name="Advanced Japanese", price=19.90)
    book_2 = Book.objects.create(name="Advanced English", price=15.45)
    url = reverse('book-list')
    response = self.client.get(url)
    serializer_data = BooksSerializer([book_1, book_2], many=True).data
    self.assertEqual(serializer_data, response.data)
    self.assertEquals(BooksSerializer(book_1).data, response.data[0])

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(200, response.status_code)
