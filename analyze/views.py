import random

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analyze.models import Analyze
from analyze.serializers import (
    AnalyzePredictSerializer,
    AnalyzeListSerializer,
    AnalyzeCreateSerializer,
    AnalyzeDetailSerializer,
    AnalyzeUpdateSerializer
)
from knowledge_base.models import Disease


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
    queryset = Analyze.objects.all()

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

