from django.urls import include, re_path
from rest_framework import routers

from .api import VideoAPI

router = routers.DefaultRouter()
router.register('videos', VideoAPI, 'videos')

urlpatterns = [
    re_path(r'^api/', include(router.urls)),
]
