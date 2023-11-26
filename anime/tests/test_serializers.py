from django.test import TestCase
from anime.models import Anime
from anime.serializers import AnimeSerializer


class AnimeSerializerTestCase(TestCase):
  def test_anime_quails(self):
    anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR')
    anime_2 = Anime.objects.create(name='Anime_2', year=2019, description="This is the worst anime of all the time", genre='AC')
    return_data = AnimeSerializer([anime_1, anime_2], many=True).data
    expected_data = [
      {
        "id": anime_1.id,
        "name": 'Anime_1',
        "year": 2009,
        "description": "This is the best anime of all the time",
        "genre": 'HR'
      },
      {
        "id": anime_2.id,
        "name": 'Anime_2',
        "year": 2019,
        "description": "This is the worst anime of all the time",
        "genre": 'AC'
      },
    ]
    
    self.assertEquals(expected_data, return_data)
