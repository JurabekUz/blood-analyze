from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import action
from weasyprint import HTML

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from analyze.filters import PatientFilter
from analyze.models import Analyze
from analyze.serializers import (
    AnalyzePredictSerializer,
    AnalyzeListSerializer,
    AnalyzeCreateSerializer,
    AnalyzeDetailSerializer,
    AnalyzeUpdateSerializer
)
from knowledge_base.models import Disease
from ml.model import predict_from_multiple_images
from logs.service import AuditLogService


CONFIDENCE_THRESHOLD = 0.75


class AnalyzePredictAPIView(GenericAPIView):
    serializer_class = AnalyzePredictSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data["images"]

        result = predict_from_multiple_images(images)

        if result["confidence"] < CONFIDENCE_THRESHOLD:
            return Response(
                {
                    "detail": (
                        "Aniqlik darajasi past. "
                        "Iltimos, sifatli va to‘g‘ri rasm(lar) yuboring."
                    ),
                    "confidence": f"Aniqlik darajasi: {result['confidence']}",
                },
                status=400
            )

        try:
            disease = Disease.objects.get(
                code=result["class_index"],
                is_active=True
            )
        except Disease.DoesNotExist:
            return Response(
                {"detail": "Kasallik bazada topilmadi"},
                status=400
            )

        # create a log
        AuditLogService.log(
            request=request,
            action="Tahlil",
            object_type="Tahlil",
            object_id=None,
            description="Tahlil yaratildi"
        )

        return Response({
            "disease": {
                "id": disease.id,
                "name": disease.name,
            },
            "accuracy": result["confidence"],
        })


class AnalyzeViewSet(ModelViewSet):
    queryset = Analyze.objects.all().order_by('-id')
    filterset_class = PatientFilter

    def get_serializer_class(self):
        if self.action == 'list':
            slz_class = AnalyzeListSerializer
        elif self.action == 'retrieve':
            slz_class = AnalyzeDetailSerializer
        elif self.action == 'create':
            slz_class = AnalyzeCreateSerializer
        else:
            slz_class = AnalyzeUpdateSerializer
        return slz_class


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        AuditLogService.log(
            request=self.request,
            action="Yaratish",
            object_type="Tahlil",
            object_id=serializer.instance.id,
            description="Tahlil yaratildi"
        )

    def perform_update(self, serializer):
        serializer.save()
        AuditLogService.log(
            request=self.request,
            action="Tahrirlash",
            object_type="Tahlil",
            object_id=serializer.instance.id,
            description="Tahlil tahrirlandi"
        )

    def perform_destroy(self, instance):
        instance_id = instance.id
        instance.delete()
        AuditLogService.log(
            request=self.request,
            action="O'chirish",
            object_type="Tahlil",
            object_id=instance_id,
            description="Tahlil o'chirildi"
        )

    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf(self, request, pk=None):
        analyze = Analyze.objects.select_related(
            'user', 'patient', 'disease'
        ).prefetch_related('images').get(pk=pk)

        html_string = render_to_string('analyze.html', {
            'user': analyze.user.get_full_name(),
            'patient': analyze.patient.get_full_name(),
            'disease': analyze.disease.name if analyze.disease else '',
            'accuracy': analyze.accuracy,
            'health_score': analyze.health_score,
            'novelty_score': analyze.novelty_score,
            'diagnostic_recommendation': analyze.diagnostic_recommendation,
            'treatment_plan': analyze.treatment_plan,
            'general_recommendations': analyze.general_recommendations,
            'images': analyze.images.all(),
            'hostname': request.get_host(),
        })

        pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        
        AuditLogService.log(
            request=request,
            action="PDF",
            object_type="Tahlil",
            object_id=analyze.id,
            description="Tahlil PDF yuklab olindi"
        )

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="analyze_{analyze.id}.pdf"'
        return response
