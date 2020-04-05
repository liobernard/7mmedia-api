from django.urls import include, re_path
from rest_framework import routers

from .api import (
    VideoAPI, LoginAPI, LogoutAPI,
    SignedUrlAPI, ListFilmsAPI, ListThumbnailsAPI,
    SignUpFormAPI
)

router = routers.DefaultRouter()
router.register('videos', VideoAPI, 'videos')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^auth/login/$', LoginAPI.as_view()),
    re_path(r'^auth/logout/$', LogoutAPI.as_view()),
    re_path(r'^email/signup_form/$', SignUpFormAPI.as_view()),
    re_path(r'^s3/list_objects/video/$', ListFilmsAPI.as_view()),
    re_path(r'^s3/list_objects/thumbnail/$', ListThumbnailsAPI.as_view()),
    re_path(r'^s3/signed_url/$', SignedUrlAPI.as_view()),
]
