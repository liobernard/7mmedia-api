import logging
from rest_framework import filters, generics, viewsets, views
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError
from django.core.mail import BadHeaderError, mail_admins
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from django_filters.rest_framework import DjangoFilterBackend
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from .filters import VideoFilter
from .models import Video
from .permissions import ReadOnly
from .serializers import (
    VideoSerializer, UserSerializer, LoginUserSerializer,
    SignedUrlSerializer, SignUpFormSerializer
)


AWS_ACCESS_KEY_ID       = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME      = config('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
SERVER_EMAIL            = config('SERVER_EMAIL')


class VideoAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|ReadOnly]
    serializer_class = VideoSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = VideoFilter
    lookup_field = 'slug'
    ordering_fields = ('published_at',)
    ordering = '-published_at'

    def get_queryset(self):
        user = self.request.user
        if user and user.is_active and user.is_staff:
            return Video.objects.all()
        return Video.objects.filter(published_at__isnull=False)

    def perform_create(self, serializer):
        user = self.request.user
        if user and user.is_active and user.is_staff:
            serializer.save(owner=self.request.user)
        else:
            raise ValidationError('Unable to create object with provided credentials.')


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class LogoutAPI(KnoxLogoutView):
    permission_classes = [IsAdminUser, IsAuthenticated]


class SignedUrlAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SignedUrlSerializer

    def create_presigned_post(self, bucket_name, object_name,
                              fields=None, conditions=None, expiration=3600):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4', region_name=AWS_S3_REGION_NAME)
        )
        try:
            response = s3_client.generate_presigned_post(
                bucket_name, object_name,
                Fields=fields, Conditions=conditions, ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bucket_name = serializer.validated_data['bucket_name']
        object_name = serializer.validated_data['object_name']
        fields      = serializer.validated_data['fields']
        conditions  = serializer.validated_data['conditions']
        expiration  = serializer.validated_data['expiration']

        response = self.create_presigned_post(
            bucket_name, object_name,
            fields, conditions, expiration
        )

        return Response({ 'url': response['url'], 'fields': response['fields'] })


class ListThumbnailsAPI(views.APIView):
    permission_classes = [IsAdminUser]

    def list_thumbnails(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4', region_name=AWS_S3_REGION_NAME)
        )

        try:
            response = s3_client.list_objects_v2(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                Prefix='media/images/film_thumbnails/'
            )['Contents']
        except KeyError as e:
            raise NotFound(detail='{e} not found.'.format(e=e))
        except ClientError as e:
            raise NotFound(detail='Error: {e}'.format(e=e))

        return list(map(
            lambda obj:
                'https://{bucket}.s3.{region}.amazonaws.com/{key}'.format(
                    bucket=AWS_STORAGE_BUCKET_NAME,
                    region=AWS_S3_REGION_NAME,
                    key=obj['Key']
                ),
            filter(
                lambda obj: obj['Key'] is not 'media/images/film_thumbnails/',
                filter(lambda obj: obj['Size'] > 0, response)
            )
        ))

    def get(self, request, *args, **kwargs):
        return Response(self.list_thumbnails())


class ListFilmsAPI(views.APIView):
    permission_classes = [IsAdminUser]

    def list_films(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4', region_name=AWS_S3_REGION_NAME)
        )

        try:
            response = s3_client.list_objects_v2(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                Prefix='media/videos/films/'
            )['Contents']
        except KeyError as e:
            raise NotFound(detail='{e} not found.'.format(e=e))
        except ClientError as e:
            raise NotFound(detail='Error: {e}'.format(e=e))

        return list(map(
            lambda obj:
                'https://{bucket}.s3.{region}.amazonaws.com/{key}'.format(
                    bucket=AWS_STORAGE_BUCKET_NAME,
                    region=AWS_S3_REGION_NAME,
                    key=obj['Key']
                ),
            filter(
                lambda obj: obj['Key'] is not 'media/videos/films/',
                filter(lambda obj: obj['Size'] > 0, response)
            )
        ))

    def get(self, request, *args, **kwargs):
        return Response(self.list_films())


class SignUpFormAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name    = serializer.validated_data['name']
        email   = serializer.validated_data['email']
        project = serializer.validated_data['project']
        message = serializer.validated_data['message']

        if name and email and project and message:
            subject = ' NEW CLIENT SIGNUP \u2014 {n}'.format(n=name)
            html_message = render_to_string('email.html', serializer.validated_data)
            plain_message = strip_tags(html_message)

            try:
                mail_admins(subject, plain_message, html_message=html_message)
            except BadHeaderError:
                return Response('Invalid header found.')
            return Response('Message sent successfully.')
        else:
            return Response('Make sure all fields are entered and valid.')

