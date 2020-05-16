from django.urls import re_path

from .api import LoginAPI, LogoutAPI

urlpatterns = [
    re_path(r'^api/auth/login/$', LoginAPI.as_view()),
    re_path(r'^api/auth/logout/$', LogoutAPI.as_view()),
]
