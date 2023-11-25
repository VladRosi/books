from django.test import TestCase
from store.logic import operations


class LogicTestCase(TestCase):
  def test_plus(self):
    res = operations(10, 20, '+')
    self.assertEqual(30, res)

  def test_minus(self):
    res = operations(99, 66, '-')
    self.assertEqual(33, res)

  def test_multiply(self):
    res = operations(3, 4, '*')
    self.assertEqual(12, res)

  # def test_division(self):
  #   res = operations(99, 33, '/')
  #   self.assertEqual(3, res)
