from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.pagination import CommonPagination
from .filters import PatientFilter
from .models import Patient
from .serializers import (
    PatientListSerializer,
    PatientRetrieveSerializer,
    PatientCreateUpdateSerializer,
    PatientSelectSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientRetrieveSerializer
    filterset_class = PatientFilter
    pagination_class = CommonPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        if self.action == 'retrieve':
            return PatientRetrieveSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PatientCreateUpdateSerializer
        if self.action == 'select':
            return PatientSelectSerializer
        return PatientRetrieveSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Soft delete → is_active = False"""
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def select(self, request):
        """
        Lightweight list for dropdowns / auto-complete.
        Supports: ?search=Abd
        """
        search = request.query_params.get("search", "")

        qs = Patient.objects.filter(is_active=True)
        if search:
            qs = qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

