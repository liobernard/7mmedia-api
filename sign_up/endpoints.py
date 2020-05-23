from django.urls import re_path

from .api import SignUpFormAPI

urlpatterns = [
    re_path(r'^email/signup_form/$', SignUpFormAPI.as_view()),
]
