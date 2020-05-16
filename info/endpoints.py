from django.urls import re_path

from .api import HomeInfoAPI, AboutInfoAPI

urlpatterns = [
    re_path(r'^api/info/home/$', HomeInfoAPI.as_view()),
    re_path(r'^api/info/about/$', AboutInfoAPI.as_view()),
]
