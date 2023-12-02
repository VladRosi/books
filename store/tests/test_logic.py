from django.test import TestCase
from django.contrib.auth.models import User
from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
  def setUp(self):
    user_1 = User.objects.create(username='user_1', password='test_password', first_name='first', last_name='last')
    user_2 = User.objects.create(username='user_2', password='test_password')
    user_3 = User.objects.create(username='user_3', password='test_password')

    self.book = Book.objects.create(owner=user_1, name="Advanced Japanese", price=19.90, author_name='Author 1', discount=15)

    UserBookRelation.objects.create(user=user_1, book=self.book, like=True, in_bookmarks=False, rate=3)
    UserBookRelation.objects.create(user=user_2, book=self.book, like=True, in_bookmarks=True, rate=5)
    UserBookRelation.objects.create(user=user_3, book=self.book, in_bookmarks=False, rate=2)

  def test_ok(self):
    set_rating(self.book)
    self.book.refresh_from_db()
    self.assertEqual('3.33', str(self.book.rating))


"""--------------------------------------------------------------------------"""

# from django.test import TestCase
# from store.logic import operations

# class LogicTestCase(TestCase):
#   def test_plus(self):
#     res = operations(10, 20, '+')
#     self.assertEqual(30, res)

#   def test_minus(self):
#     res = operations(99, 66, '-')
#     self.assertEqual(33, res)

#   def test_multiply(self):
#     res = operations(3, 4, '*')
#     self.assertEqual(12, res)

#   # def test_division(self):
#   #   res = operations(99, 33, '/')
#   #   self.assertEqual(3, res)
