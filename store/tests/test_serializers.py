from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
  def test_ok(self):
    book_1 = Book.objects.create(name="Advanced Japanese", price=19.90)
    book_2 = Book.objects.create(name="Advanced English", price=15.45)
    book_3 = Book.objects.create(name="I and my ass", price=19)
    data = BooksSerializer([book_1, book_2, book_3], many=True).data
    expected_data = [
      {
        'id': book_1.id,
        'name': 'Advanced Japanese',
        'price': '19.90'
      },
      {
        'id': book_2.id,
        'name': 'Advanced English',
        'price': '15.45'
      },
      {
        'id': book_3.id,
        'name': 'I and my ass',
        'price': '19.00'
      },
    ]
    self.assertEquals(expected_data, data)
