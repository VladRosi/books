from rest_framework.routers import SimpleRouter
from .views import AnimeViewSet

router = SimpleRouter()
router.register(r'animes', AnimeViewSet)

urlpatterns = []

urlpatterns += router.urls