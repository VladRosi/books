from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from anime.models import Anime
from anime.serializers import AnimeSerializer


class AnimeApiTestCase(APITestCase):
  def setUp(self):
    self.anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR')
    self.anime_2 = Anime.objects.create(name='Anime_2', year=2011, description="This is the worst anime of all the time", genre='RM')
    self.anime_3 = Anime.objects.create(name='Anime_3', year=2014, description="This is the worst anime of all the time", genre='AC')
    self.anime_4 = Anime.objects.create(name='Anime_4', year=2014, description="This is the worst anime of all the time", genre='AC')
    self.anime_5 = Anime.objects.create(name='Anime_5', year=2020, description="This is the worst anime of all the time", genre='TR')

    self.url = reverse('anime-list')

  def test_get(self):
    resp = self.client.get(self.url, data={'year': 2014})
    data = AnimeSerializer([self.anime_3, self.anime_4], many=True).data
    self.assertEquals(data, resp.data)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)

  def test_ordering(self):
    self.url = reverse('anime-list')
    resp = self.client.get(self.url, data={'ordering': '-year'})
    data = AnimeSerializer(self.anime_5).data
    self.assertEquals(data, resp.data[0])
    self.assertEqual(status.HTTP_200_OK, resp.status_code)

  def test_search(self):
    self.url = reverse('anime-list')
    resp = self.client.get(self.url, data={'search': 'Anime_2'})
    data = AnimeSerializer(self.anime_2).data
    self.assertEquals(data, resp.data[0])
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
