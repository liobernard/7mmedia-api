from django.urls import re_path

from .api import HomeInfoAPI, AboutInfoAPI

urlpatterns = [
    re_path(r'^info/home/$', HomeInfoAPI.as_view()),
    re_path(r'^info/about/$', AboutInfoAPI.as_view()),
]
