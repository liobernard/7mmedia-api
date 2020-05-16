from django.db.models import CharField, TextField, OneToOneField, SET_DEFAULT
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel

from videos.models import Video

def get_latest_video_pk():
    return Video.objects.latest().pk

class HomeInfo(SingletonModel):
    facebook_url = CharField(_('facebook_url'), max_length=255, blank=True)

    instagram_url = CharField(_('instagram_url'), max_length=255, blank=True)

    twitter_url = CharField(_('twitter_url'), max_length=255, blank=True)

    video_banner_url = TextField(_('video_banner_url'))

    logo_url = TextField(_('logo_url'))

    info_1 = CharField(_('info_1'), max_length=255, blank=True)

    info_2 = CharField(_('info_2'), max_length=255, blank=True)

    featured_video = OneToOneField(
        Video,
        default=get_latest_video_pk,
        on_delete=SET_DEFAULT,
    )

    class Meta:
        verbose_name = _('Home Page Info')

    def __str__(self):
        return 'Home Page Info'

    def get_info_name(self):
        return 'home'


class AboutInfo(SingletonModel):
    text = TextField(_('text'))

    photo_url = TextField(_('photo_url'))

    showreel_url = TextField(_('showreel_url'))

    class Meta:
        verbose_name = _('About Page Info')

    def __str__(self):
        return 'About Page Info'

    def get_info_name(self):
        return 'about'
