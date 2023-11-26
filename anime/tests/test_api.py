from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from anime.models import Anime
from anime.serializers import AnimeSerializer


class AnimeApiTestCase(APITestCase):
  def test_get(self):
    anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR')
    anime_2 = Anime.objects.create(name='Anime_2', year=2019, description="This is the worst anime of all the time", genre='AC')
    url = reverse('anime-list')
    resp = self.client.get(url)

    data = AnimeSerializer([anime_1, anime_2], many=True).data

    self.assertEquals(data, resp.data)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
