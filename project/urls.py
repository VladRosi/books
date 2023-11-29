from django.contrib import admin
from django.urls import path, include, re_path
from store.views import auth
# from rest_framework.authtoken import views

urlpatterns = [
  path("admin/", admin.site.urls),
  # path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
  path('api/store/', include('store.urls')),
  path('api/anime/', include('anime.urls')),
  re_path('', include('social_django.urls', namespace='social')),
  path('auth/', auth, name='oauth')
]
