import logging
import magic
import requests
from decouple import config
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, ValidationError

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


AWS_ACCESS_KEY_ID       = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME      = config('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_CDN_DOMAIN          = config('AWS_CDN_DOMAIN')


class S3API(APIView):
    permission_classes = [IsAdminUser]

    def get_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(
                signature_version='s3v4', region_name=AWS_S3_REGION_NAME
            )
        )

    def list_objects(self):
        s3_client = self.get_s3_client()

        try:
            response = s3_client.list_objects_v2(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                Prefix=self.prefix
            )['Contents']
        except KeyError as e:
            raise NotFound(detail='{} not found.'.format(e))
        except ClientError as e:
            raise NotFound(detail='Error: {}'.format(e))

        return list(map(
            lambda obj: 'https://' + AWS_CDN_DOMAIN + '/' + obj['Key'],
            filter(
                lambda obj: obj['Key'] is not self.prefix,
                filter(lambda obj: obj['Size'] > 0, response)
            )
        ))

    def validate_file(self, file):
        magic_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)

        if magic_type != self.content_type:
            main, sub = self.content_type.split('/', 1)
            if (main != magic_type.split('/')[0] and sub != '*'):
                raise ValidationError(
                    'Error: Only {t} types supported. You '
                    'submitted {s}.'.format(t=self.content_type, s=magic_type)
                )
        return file

    def create_presigned_post(self, object_name):
        s3_client = self.get_s3_client()

        try:
            response = s3_client.generate_presigned_post(
                AWS_STORAGE_BUCKET_NAME,
                object_name,
                Fields={'acl': 'public-read'},
                Conditions=[{'acl': 'public-read'}],
                ExpiresIn=3600
            )
        except ClientError as e:
            logging.error(e)
            return None
        return response

    def get(self, request, *args, **kwargs):
        objects = self.list_objects()
        return Response(objects)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content.')

        unvalidated = request.data['file']
        file        = self.validate_file(unvalidated)
        object_name = self.prefix + file.name
        response    = self.create_presigned_post(object_name)

        return Response({'url': response['url'], 'fields': response['fields']})


class S3VideosAPI(S3API):
    prefix          = 'media/videos/'
    content_type    = 'video/mp4'


class S3FilmsAPI(S3API):
    prefix          = 'media/videos/films/'
    content_type    = 'video/mp4'


class S3ImagesAPI(S3API):
    prefix          = 'media/images/'
    content_type    = 'image/*'


class S3FilmThumbnailsAPI(S3API):
    prefix          = 'media/images/film_thumbnails/'
    content_type    = 'image/*'
