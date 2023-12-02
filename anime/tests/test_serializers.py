from django.contrib.auth.models import User
from django.db.models import Case, Count, When
from django.test import TestCase
from anime.models import Anime, Review, UserAnimeRelation
from anime.serializers import AnimeSerializer


class AnimeSerializerTestCase(TestCase):
  def test_anime_quails(self):
    self.user_1 = User.objects.create(username='user_1', password='test_password')
    self.user_2 = User.objects.create(username='user_2', password='test_password')
    self.user_3 = User.objects.create(username='user_3', password='test_password')

    anime_1 = Anime.objects.create(creator=self.user_1, name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR')
    anime_2 = Anime.objects.create(creator=self.user_1, name='Anime_2', year=2019, description="This is the worst anime of all the time", genre='AC')

    UserAnimeRelation.objects.create(user=self.user_1, anime=anime_1, like=True, in_bookmarks=True)
    UserAnimeRelation.objects.create(user=self.user_2, anime=anime_1, like=True, in_bookmarks=True)
    UserAnimeRelation.objects.create(user=self.user_3, anime=anime_1, like=True, in_bookmarks=True)
    UserAnimeRelation.objects.create(user=self.user_1, anime=anime_2)
    UserAnimeRelation.objects.create(user=self.user_2, anime=anime_2, like=False, in_bookmarks=False)
    UserAnimeRelation.objects.create(user=self.user_3, anime=anime_2, like=True, in_bookmarks=True)

    Review.objects.create(creator=self.user_1, anime=anime_1, title='Review 1', text='Review Text', rate=6)
    Review.objects.create(creator=self.user_1, anime=anime_2, title='Review 2', text='Review Text', rate=5)

    # return_data = AnimeSerializer([anime_1, anime_2], many=True).data
    animes = Anime.objects.all().annotate(likes=Count(Case(When(useranimerelation__like=True, then=1)))).order_by('id')
    data = AnimeSerializer(animes, many=True)
    expected_data = [
      {
        "id": anime_1.id,
        "name": 'Anime_1',
        "year": 2009,
        "description": "This is the best anime of all the time",
        "genre": 'HR',
        'reviews_count': 1,
        'likes': 3
      },
      {
        "id": anime_2.id,
        "name": 'Anime_2',
        "year": 2019,
        "description": "This is the worst anime of all the time",
        "genre": 'AC',
        'reviews_count': 1,
        'likes': 1
      },
    ]

    self.assertEquals(expected_data, data.data)
