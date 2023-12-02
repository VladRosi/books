import json
from django.contrib.auth.models import User
from django.db.models import Case, Count, When
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from anime.models import Anime, Review, UserAnimeRelation
from anime.serializers import AnimeSerializer


class AnimeApiTestCase(APITestCase):
  def setUp(self):
    self.url = reverse('anime-list')
    self.user = User.objects.create(username="test_user", password="test_password")
    self.another_user = User.objects.create(username='another_test_user', password='test_password')
    self.staff_user = User.objects.create(username='staff_test_user', password='test_password', is_staff=True)

    self.anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR', creator=self.user)
    self.anime_2 = Anime.objects.create(name='Anime_2', year=2011, description="This is the worst anime of all the time", genre='RM', creator=self.user)
    self.anime_3 = Anime.objects.create(name='Anime_3', year=2014, description="This is the worst anime of all the time", genre='AC', creator=self.user)
    self.anime_4 = Anime.objects.create(name='Anime_4', year=2014, description="This is the worst anime of all the time", genre='AC', creator=self.user)
    self.anime_5 = Anime.objects.create(name='Anime_5', year=2020, description="This is the worst anime of all the time", genre='TR', creator=self.user)

  def test_get(self):
    resp = self.client.get(self.url, data={'year': 2014})
    animes = Anime.objects.filter(year__in=[2014]).annotate(likes=Count(Case(When(useranimerelation__like=True, then=1))))  #.order_by('id')
    data = AnimeSerializer(animes, many=True).data
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEquals(data, resp.data)

  def test_get_detail(self):
    detail_url = reverse("anime-detail", args=(self.anime_5.id, ))
    resp = self.client.get(detail_url, type='application/json')
    animes = Anime.objects.filter(id__in=[self.anime_5.id]).annotate(likes=Count(Case(When(useranimerelation__like=True, then=1))))  #.order_by('id')
    data = AnimeSerializer(animes, many=True).data
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEquals(data[0], resp.data)

  def test_ordering(self):
    self.url = reverse('anime-list')
    resp = self.client.get(self.url, data={'ordering': '-year'})
    animes = Anime.objects.all().annotate(likes=Count(Case(When(useranimerelation__like=True, then=1)))).order_by('-year')
    data = AnimeSerializer(animes, many=True).data
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEquals(data, resp.data)

  def test_search(self):
    self.url = reverse('anime-list')
    resp = self.client.get(self.url, data={'search': 'Anime_2'})
    animes = Anime.objects.filter(id__in=[self.anime_2.id]).annotate(likes=Count(Case(When(useranimerelation__like=True, then=1))))
    data = AnimeSerializer(animes, many=True).data
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEquals(data, resp.data)

  def test_create(self):
    self.assertEqual(5, Anime.objects.all().count())
    self.client.force_login(self.user)
    data = {"name": "HxH", "year": 2011, "description": "Hisoka is the coolest villain", "genre": "AC"}
    json_data = json.dumps(data)
    resp = self.client.post(self.url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
    self.assertEqual(6, Anime.objects.all().count())

  def test_update(self):
    self.client.force_login(self.user)
    data = {"name": self.anime_5.name, "year": 1111, "description": self.anime_5.description, "genre": self.anime_5.genre}
    json_data = json.dumps(data)
    detail_url = reverse('anime-detail', args=(self.anime_5.id, ))
    resp = self.client.put(detail_url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.anime_5.refresh_from_db()
    self.assertEqual(1111, self.anime_5.year)

  def test_update_not_creator(self):
    self.client.force_login(self.another_user)
    data = {"name": self.anime_5.name, "year": 1111, "description": self.anime_5.description, "genre": self.anime_5.genre}
    json_data = json.dumps(data)
    detail_url = reverse('anime-detail', args=(self.anime_5.id, ))
    resp = self.client.put(detail_url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)
    self.anime_5.refresh_from_db()
    self.assertEqual(2020, self.anime_5.year)

  def test_update_not_creator_but_staff(self):
    self.client.force_login(self.staff_user)
    data = {"name": self.anime_5.name, "year": 1111, "description": self.anime_5.description, "genre": self.anime_5.genre}
    json_data = json.dumps(data)
    detail_url = reverse('anime-detail', args=(self.anime_5.id, ))
    resp = self.client.put(detail_url, data=json_data, content_type='application/json')
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.anime_5.refresh_from_db()
    self.assertEqual(1111, self.anime_5.year)

  def test_delete(self):
    self.assertEqual(5, Anime.objects.all().count())
    self.client.force_login(self.user)
    detail_url = reverse('anime-detail', args=(self.anime_5.id, ))
    resp = self.client.delete(detail_url)
    self.assertEqual(status.HTTP_204_NO_CONTENT, resp.status_code)
    self.assertEqual(4, Anime.objects.all().count())


class UserAnimeRelationApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username="test_user", password="test_password")
    self.another_user = User.objects.create(username='another_test_user', password='test_password')
    self.staff_user = User.objects.create(username='staff_test_user', password='test_password', is_staff=True)

    self.anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR', creator=self.user)
    self.anime_2 = Anime.objects.create(name='Anime_2', year=2011, description="This is the worst anime of all the time", genre='RM', creator=self.user)

    self.url = reverse('useranimerelation-detail', args=(self.anime_1.id, ))

  def test_have_like(self):
    data = {'like': True}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = UserAnimeRelation.objects.get(user=self.user, anime=self.anime_1)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertTrue(relation.like)

  def test_in_bookmarks(self):
    data = {'in_bookmarks': True}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = UserAnimeRelation.objects.get(user=self.user, anime=self.anime_1)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertTrue(relation.in_bookmarks)


class ReviewApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username="test_user", password="test_password")
    self.another_user = User.objects.create(username='another_test_user', password='test_password')
    self.staff_user = User.objects.create(username='staff_test_user', password='test_password', is_staff=True)

    self.anime_1 = Anime.objects.create(name='Anime_1', year=2009, description="This is the best anime of all the time", genre='HR', creator=self.user)
    self.anime_2 = Anime.objects.create(name='Anime_2', year=2011, description="This is the worst anime of all the time", genre='RM', creator=self.user)

    self.url = reverse('review-detail', args=(self.anime_1.id, ))

  def test_have_rate(self):
    data = {'rate': 9}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = Review.objects.get(creator=self.user, anime=self.anime_1)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEqual(9, relation.rate)

  def test_have_rate_wrong(self):
    data = {'rate': 19}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = Review.objects.get(creator=self.user, anime=self.anime_1)
    self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
    self.assertEqual(5, relation.rate)

  def test_have_rate(self):
    data = {'text': 'Hello World'}
    json_data = json.dumps(data)
    self.client.force_login(self.user)
    resp = self.client.patch(self.url, data=json_data, content_type='application/json')
    relation = Review.objects.get(creator=self.user, anime=self.anime_1)
    self.assertEqual(status.HTTP_200_OK, resp.status_code)
    self.assertEqual('Hello World', relation.text)
