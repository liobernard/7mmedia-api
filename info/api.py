from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import HomeInfo, AboutInfo
from .serializers import (
    HomeInfoSerializer,
    PutHomeInfoSerializer,
    AboutInfoSerializer,
)
from utils.permissions import IsAdminOrReadOnly


class InfoAPI(GenericAPIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_info(self):
        assert self.info is not None, (
            "'%s' should include a `info` attribute."
            % self.__class__.__name__
        )
        info = self.info
        return info.objects.get()

    def get(self, request, *args, **kwargs):
        info = self.get_info()
        serializer = self.get_serializer(info)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        info = self.get_info()
        serializer = self.get_serializer(info, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class HomeInfoAPI(InfoAPI):
    info = HomeInfo
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return PutHomeInfoSerializer
        return HomeInfoSerializer

class AboutInfoAPI(InfoAPI):
    info = AboutInfo
    serializer_class = AboutInfoSerializer
