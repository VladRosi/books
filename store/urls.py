from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import BookViewSet

router = SimpleRouter()
router.register(r'book', BookViewSet)

urlpatterns = [
  # path('books/', include(router.urls))
]

urlpatterns += router.urls
