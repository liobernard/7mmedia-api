from django_filters import rest_framework as django_filters
from .models import Video

class VideoFilter(django_filters.FilterSet):
    featured = django_filters.BooleanFilter(
        field_name='featured',
        method='filter_featured'
    )

    published = django_filters.BooleanFilter(
        field_name='published_at',
        method='filter_published'
    )

    exclude = django_filters.CharFilter(
        field_name='slug',
        exclude=True
    )

    def filter_featured(self, queryset, name, value):
        if value == False:
            return queryset.filter(featured=False)
        elif value == True:
            return queryset.filter(featured=True)
        return queryset

    def filter_published(self, queryset, name, value):
        if value == False:
            return queryset.filter(published_at__isnull=True)
        elif value == True:
            return queryset.filter(published_at__isnull=False)
        return queryset

    class Meta:
        model = Video
        fields = ['featured', 'published', 'exclude']
