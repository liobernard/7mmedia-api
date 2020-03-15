import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from decouple import config

from .models import Video


AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')


class VideoSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.is_staff:
            return user
        raise serializers.ValidationError('Unable to log in with provided credentials.')


class SignedUrlSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(default=AWS_STORAGE_BUCKET_NAME)
    object_name = serializers.CharField()

    fields = serializers.JSONField(
        allow_null=True,
        default={ 'acl': 'public-read' }
    )

    conditions = serializers.JSONField(
        allow_null=True,
        default=[{ 'acl': 'public-read' }]
    )

    expiration = serializers.IntegerField(default=3600)


class SignUpFormSerializer(serializers.Serializer):
    name    = serializers.CharField()
    email   = serializers.CharField()
    project = serializers.CharField()
    message = serializers.CharField()

    def get_email_regex(self):
        return '^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$'

    def get_project_options(self):
        return [
            'Wedding, entertainment, or special event',
            'Commercial or promotional work',
            'Documentary or artistic project',
            'Other'
        ]

    def validate_email(self, email):
        if (re.search(self.get_email_regex(), email) == None):
            raise serializers.ValidationError('Invalid email address provided.')
        return email

    def validate_project(self, project):
        if (project not in self.get_project_options()):
            raise serializers.ValidationError('Invalid project selected.')
        return project
