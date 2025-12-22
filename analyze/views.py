import random

from django.db.models import Count, Avg
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
from patient.models import Patient


class AnalyzePredictAPIView(GenericAPIView):
    serializer_class = AnalyzePredictSerializer

    def post(self, request):
        serializer = AnalyzePredictSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        diseases = Disease.objects.filter(is_active=True)
        if not diseases.exists():
            return Response({"detail": "No active diseases found."}, status=400)

        disease = random.choice(list(diseases))
        accuracy = round(random.uniform(0.8, 0.9), 3)

        return Response({
            "disease": {"name": disease.name, "id": disease.id},
            "accuracy": accuracy,
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

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="analyze_{analyze.id}.pdf"'
        return response
