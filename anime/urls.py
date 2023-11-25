from rest_framework.routers import SimpleRouter
from .views import AnimeViewSet

router = SimpleRouter()
router.register(r'anime_list', AnimeViewSet)

urlpatterns = []

urlpatterns += router.urls