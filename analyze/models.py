from django.db import models

from knowledge_base.models import Media, Disease
from patient.models import Patient

# Create your models here.

"""
0. kasallik nomi modeli,: CRUD + select api. fields: name, id, is_active, created_at, updated_at. created_by, tavsif (text field).

1. media model yaratish, 2 ta api create va delete. multiple image create funksiyasi. 
fieldlari: name, id, file (image field): name ni save methodi ichida avto berish kerak max 50 ta belgi.

2. Analyze model yaratish:
fieldlar: 
created_at, user, images (many to many field), patient, 
kasallik nomi,  - bu field relation field.
aniqlik darajasi - 0-1 orligida 
Sog’lomlik indeksi – 0-1 oralig'ida
Anomaliya yoki yangilik indeksi – 0-1 oralig'ida
diagnostik tavsiya - text field
davolash ko'rsatmasi (text field)
umumiy tavsiyalar (text field)

CRUD api chiqarish kerak. 
shifokor create qiladi. 
shifokor bemorni va rasmlarni yuboradi, api kasallik  nomi va id sini qaytaradi, va anilik darajasini. Lekin analyze modelida object yaratilmaydi.
qolgan maydonlarni kiritib keyin post qiladi shunda object yaratiladi.
tahrirlash mavjud faqat, user, rasmlar, kasallik nomi va aniqlik darajasini tahrirlay olmaydi.
admin rasm orqali anaylze qilolmaydi lekin ko'ra oladi, va tahrirlay oladi.

"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Analyze(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyzes'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='analyzes'
    )
    images = models.ManyToManyField(Media, related_name='analyzes')

    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        related_name='analyzes',
        null=True,
        blank=True
    )

    accuracy = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        null=True,
        blank=True
    )

    health_score = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        null=True,
        blank=True
    )

    novelty_score = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        null=True,
        blank=True
    )

    diagnostic_recommendation = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    general_recommendations = models.TextField(blank=True)

    def __str__(self):
        return f"Analyze #{self.id} – {self.patient}"

