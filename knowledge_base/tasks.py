from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Media


@shared_task
def clean_unused_media():
    """
    O'zi mavjud, lekin hech qayerda ishlatilmayotgan media fayllarni o'chiradi.
    Shart: Media modeli hech qanday boshqa modelga FK yoki M2M bilan bog'lanmagan bo'lsa.
    """

    # Masalan: 1 kun oldin yaratilgan, lekin hali ishlatilmagan
    cutoff = timezone.now() - timedelta(days=1)

    unused_files = Media.objects.filter(
        created_at__lt=cutoff
    )

    count = unused_files.count()

    for media in unused_files:
        # Faylni file systemdan o'chirish
        if media.file:
            media.file.delete(save=False)
        media.delete()

    return f"Cleaned {count} unused media files"
