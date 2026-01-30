from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = (
            'id',
            'user',
            'user_full_name',
            'action',
            'object_type',
            'object_id',
            'description',
            'ip_address',
            'created_at',
        )

    def get_user_full_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return None
