from django.urls import re_path

from .api import ListFilmsAPI, ListThumbnailsAPI, SignedUrlAPI

urlpatterns = [
    re_path(r'^api/s3/list_objects/video/$', ListFilmsAPI.as_view()),
    re_path(r'^api/s3/list_objects/thumbnail/$', ListThumbnailsAPI.as_view()),
    re_path(r'^api/s3/signed_url/$', SignedUrlAPI.as_view()),
]
