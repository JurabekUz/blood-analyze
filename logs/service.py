from logs.models import AuditLog


class AuditLogService:
    @staticmethod
    def log(
        *,
        request,
        action: str,
        object_type: str,
        object_id: int | None = None,
        description: str = ""
    ):
        """
        Universal audit logger.

        request      → DRF request
        action       → Yaratish / Tahrirlash / O'chirish / Login / PDF
        object_type  → Model yoki biznes obyekt nomi
        object_id    → Obyekt ID (ixtiyoriy)
        description  → Inson o‘qiydigan izoh
        """

        user = getattr(request, "user", None)

        AuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            object_type=object_type,
            object_id=object_id,
            description=description,
            ip_address=AuditLogService._get_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")
        )

    @staticmethod
    def _get_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
