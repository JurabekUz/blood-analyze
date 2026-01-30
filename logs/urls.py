from rest_framework.routers import DefaultRouter
from logs.views import AuditLogViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
