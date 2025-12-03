from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Disease, Media
from .serializers import (
    DiseaseSerializer,
    DiseaseCreateUpdateSerializer, MultipleMediaCreateSerializer, MediaSerializer, DiseaseListSerializer
)
from utils.serializers import IdNameSerializer, SelectSerializer


class DiseaseViewSet(ModelViewSet):
    queryset = Disease.objects.filter(is_active=True).order_by("-id")
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DiseaseSerializer
        if self.action in ["create", "update", "partial_update"]:
            return DiseaseCreateUpdateSerializer
        return DiseaseListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=False, methods=["get"])
    def select(self, request):
        serializer = SelectSerializer(self.queryset, many=True)
        return Response(serializer.data)


class MediaCreateView(GenericAPIView):
    serializer_class = MediaSerializer

    def post(self, request):
        serializer = MediaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MediaDeleteView(DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
