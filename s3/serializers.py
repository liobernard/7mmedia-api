from decouple import config
from rest_framework.serializers import (
    Serializer, CharField, JSONField, IntegerField
)

AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

class SignedUrlSerializer(Serializer):
    bucket_name = CharField(default=AWS_STORAGE_BUCKET_NAME)
    object_name = CharField()

    fields = JSONField(
        allow_null=True,
        default={ 'acl': 'public-read' }
    )

    conditions = JSONField(
        allow_null=True,
        default=[{ 'acl': 'public-read' }]
    )

    expiration = IntegerField(default=3600)
