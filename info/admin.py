from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import HomeInfo, AboutInfo

admin.site.register(HomeInfo, SingletonModelAdmin)
admin.site.register(AboutInfo, SingletonModelAdmin)
