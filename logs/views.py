from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.permissions import IsAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer
from .filters import AuditLogFilter


class AuditLogViewSet(ReadOnlyModelViewSet):
    """
    Audit Log API
    - Admin: barcha loglarni ko‘radi
    - Oddiy user: faqat o‘z loglarini ko‘radi
    """

    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = AuditLogFilter

    search_fields = [
        'description',
        'action',
    ]

    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = AuditLog.objects.select_related('user')
        return qs
