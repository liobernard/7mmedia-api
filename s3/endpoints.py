from django.urls import re_path

from .api import S3VideosAPI, S3FilmsAPI, S3ImagesAPI, S3FilmThumbnailsAPI

urlpatterns = [
    re_path(r'^s3/media/videos/$', S3VideosAPI.as_view()),
    re_path(r'^s3/media/videos/films/$', S3FilmsAPI.as_view()),
    re_path(r'^s3/media/images/$', S3ImagesAPI.as_view()),
    re_path(r'^s3/media/images/film_thumbnails/$', S3FilmThumbnailsAPI.as_view()),
]
