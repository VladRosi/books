from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from anime.views import AnimeViewSet, ReviewView, UserAnimeRelationView
from store.views import BookViewSet, UserBooksRelationView, auth
# from rest_framework.authtoken import views

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBooksRelationView)
router.register(r'animes', AnimeViewSet)
router.register(r'anime_relation', UserAnimeRelationView)
router.register(r'anime_review', ReviewView)

urlpatterns = [
  path("admin/", admin.site.urls),
  # path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
  path('api/store/', include('store.urls')),
  path('api/anime/', include('anime.urls')),
  re_path('', include('social_django.urls', namespace='social')),
  path('auth/', auth, name='oauth'),
  path('__debug__/', include('debug_toolbar.urls'))
]

urlpatterns += router.urls