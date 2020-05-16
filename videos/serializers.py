from rest_framework.serializers import ModelSerializer
from .models import Video

class FeaturedVideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id',
            'slug',
            'subtitle',
            'thumbnail_url',
            'title',
            'video_url',
        )

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id',
            'business_name',
            'business_website',
            'description',
            'extra_field_1',
            'extra_field_2',
            'extra_field_3',
            'extra_field_4',
            'extra_field_5',
            'featured',
            'published_at',
            'slug',
            'subtitle',
            'thumbnail_url',
            'title',
            'video_url',
        )
