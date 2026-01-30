from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from logs.service import AuditLogService

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

        AuditLogService.log(
            request=self.request,
            action="Yaratish",
            object_type="Tahlil turi",
            object_id=serializer.instance.id,
            description="Tahlil turi yaratildi"
        )

    def perform_update(self, serializer):
        serializer.save()

        AuditLogService.log(
            request=self.request,
            action="Tahrirlash",
            object_type="Tahlil turi",
            object_id=serializer.instance.id,
            description="Tahlil turi tahrirlandi"
        )


    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

        AuditLogService.log(
            request=self.request,
            action="O'chirish",
            object_type="Tahlil turi",
            object_id=instance.id,
            description="Tahlil turi o'chirildi"
        )

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

        AuditLogService.log(
            request=self.request,
            action="Yaratish",
            object_type="Media",
            object_id=serializer.instance.id,
            description="Media fayl yuklandi"
        )
        return Response(serializer.data)


class MediaDeleteView(DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def perform_destroy(self, instance):
        instance_id = instance.id
        instance.delete()

        AuditLogService.log(
            request=self.request,
            action="O'chirish",
            object_type="Media",
            object_id=instance_id,
            description="Media fayl o'chirildi"
        )
