from itertools import chain
from django.conf.urls import re_path, include
from django.contrib import admin

from videos import endpoints as videos
from info import endpoints as info
from auth import endpoints as auth
from s3 import endpoints as s3
from sign_up import endpoints as sign_up

urlpatterns = [
    re_path(r'^api/', include(videos)),
    re_path(r'^api/', include(info)),
    re_path(r'^api/', include(auth)),
    re_path(r'^api/', include(s3)),
    re_path(r'^api/', include(sign_up)),
    re_path(r'^api/admin/', admin.site.urls),
]