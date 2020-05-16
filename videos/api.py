from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .filters import VideoFilter
from .models import Video
from .serializers import VideoSerializer
from utils.permissions import IsAdminOrReadOnly


class VideoAPI(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = VideoSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
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
