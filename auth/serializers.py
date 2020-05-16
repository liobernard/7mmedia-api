from rest_framework.serializers import (
    Serializer, ModelSerializer, CharField, ValidationError,
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class LoginUserSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.is_staff:
            return user
        raise ValidationError('Unable to log in with provided credentials.')
