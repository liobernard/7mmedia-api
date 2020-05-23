from django.urls import include, re_path
from rest_framework import routers

from .api import VideoAPI

router = routers.SimpleRouter()
router.register('videos', VideoAPI, 'videos')

urlpatterns = [
    re_path('', include(router.urls)),
]
