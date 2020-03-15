from django.conf.urls import re_path, include
from django.contrib import admin

from videos import endpoints

urlpatterns = [
    re_path(r'^api/', include(endpoints)),
    re_path(r'^api/admin/', admin.site.urls),
    re_path(r'^api/auth/', include('knox.urls')),
]