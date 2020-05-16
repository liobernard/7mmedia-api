from itertools import chain
from django.conf.urls import re_path, include
from django.contrib import admin

from videos import endpoints as videos
from info import endpoints as info
from auth import endpoints as auth
from s3 import endpoints as s3
from sign_up import endpoints as sign_up

urlpatterns = [
    re_path(r'^', include(videos)),
    re_path(r'^', include(info)),
    re_path(r'^', include(auth)),
    re_path(r'^', include(s3)),
    re_path(r'^', include(sign_up)),
    re_path(r'^api/admin/', admin.site.urls),
]