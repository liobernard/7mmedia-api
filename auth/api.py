from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView

from .serializers import UserSerializer, LoginUserSerializer


class LoginAPI(GenericAPIView):
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
    permission_classes = [IsAdminUser]
