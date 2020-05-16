import logging
from decouple import config
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from .serializers import SignedUrlSerializer


AWS_ACCESS_KEY_ID       = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME      = config('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')


class SignedUrlAPI(GenericAPIView):
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


class ListThumbnailsAPI(APIView):
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
                'https://assets.7mmedia.online/{key}'.format(key=obj['Key']),
            filter(
                lambda obj: obj['Key'] is not 'media/images/film_thumbnails/',
                filter(lambda obj: obj['Size'] > 0, response)
            )
        ))

    def get(self, request, *args, **kwargs):
        return Response(self.list_thumbnails())


class ListFilmsAPI(APIView):
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
                'https://assets.7mmedia.online/{key}'.format(key=obj['Key']),
            filter(
                lambda obj: obj['Key'] is not 'media/videos/films/',
                filter(lambda obj: obj['Size'] > 0, response)
            )
        ))

    def get(self, request, *args, **kwargs):
        return Response(self.list_films())
