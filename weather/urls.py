from .views import WeatherViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', WeatherViewSet, basename='weather')

urlpatterns = [
]
urlpatterns += router.urls
