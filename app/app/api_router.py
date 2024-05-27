from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from keydo_api.views import KeystrokeViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("keystrokes", KeystrokeViewSet)


app_name = "api"
urlpatterns = router.urls