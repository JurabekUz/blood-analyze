from django.db import models



class AuditLog(models.Model):
    # Kim bajardi
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    # Nima qilindi
    action = models.CharField(
        max_length=100,
        help_text="CREATE_ANALYZE, UPDATE_ANALYZE, LOGIN, EXPORT_PDF, UPLOAD_MEDIA"
    )

    # Qaysi obyektga nisbatan
    object_type = models.CharField(
        max_length=100,
        help_text="Analyze, Patient, Media, Disease"
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)

    # Qo‘shimcha ma’lumot
    description = models.TextField(blank=True)

    # Texnik metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

