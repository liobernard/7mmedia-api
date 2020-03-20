from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Video(models.Model):
    owner = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE, null=True)

    business_name = models.CharField(_('business_name'), max_length=255, blank=True)

    business_website = models.CharField(_('business_website'), max_length=255, blank=True)

    description = models.TextField(_('description'), max_length=500)

    extra_field_1 = models.CharField(_('extra_field_1'), max_length=255, blank=True)

    extra_field_2 = models.CharField(_('extra_field_2'), max_length=255, blank=True)

    extra_field_3 = models.CharField(_('extra_field_3'), max_length=255, blank=True)

    extra_field_4 = models.CharField(_('extra_field_4'), max_length=255, blank=True)

    extra_field_5 = models.CharField(_('extra_field_5'), max_length=255, blank=True)

    featured = models.BooleanField(_('featured'), default=False)

    published_at = models.DateTimeField(_('published_at'), blank=True, null=True)

    slug = models.SlugField(_('slug'), unique=True, null=False, blank=True, max_length=255)

    subtitle = models.CharField(_('subtitle'), max_length=255, blank=True)

    thumbnail_url = models.TextField(_('thumbnail_url'), blank=True)

    title = models.CharField(_('title'), max_length=255)

    video_url = models.TextField(_('video_url'))

    class Meta:
        ordering = ['-published_at']
        get_latest_by = 'published_at'
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
