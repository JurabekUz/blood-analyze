from django.db import models
from users.models import User


class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


def upload_media_path(instance, filename):
    return f"media/{filename}"


class Media(models.Model):
    name = models.CharField(max_length=50, blank=True)
    file = models.ImageField(upload_to=upload_media_path)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name:
            original = self.file.name.split("/")[-1]
            clean_name = original[:50]
            self.name = clean_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
