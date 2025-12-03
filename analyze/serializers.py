from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer

from analyze.models import Analyze
from knowledge_base.models import Media
from knowledge_base.serializers import MediaSerializer
from patient.models import Patient
from patient.serializers import PatientFullNameSerializer
from users.serializers import UserFullNameSerializer
from utils.serializers import IdNameSerializer


class AnalyzePredictSerializer(Serializer):
    patient = PrimaryKeyRelatedField(queryset=Patient.objects.filter(is_active=True))
    images = PrimaryKeyRelatedField(queryset=Media.objects.all(), many=True)


class AnalyzeCreateSerializer(ModelSerializer):
    class Meta:
        model = Analyze
        exclude = ['user']


class AnalyzeUpdateSerializer(ModelSerializer):
    class Meta:
        model = Analyze
        fields = [
            'health_score', 'novelty_score',
            'diagnostic_recommendation', 'treatment_plan', 'general_recommendations'
        ]


class AnalyzeListSerializer(ModelSerializer):
    user = UserFullNameSerializer()
    patient = PatientFullNameSerializer()
    disease = IdNameSerializer(allow_null=True)

    class Meta:
        model = Analyze
        fields = ['id', 'user', 'patient', 'created_at', 'disease']


class AnalyzeDetailSerializer(ModelSerializer):
    user = UserFullNameSerializer()
    patient = PatientFullNameSerializer()
    disease = IdNameSerializer(allow_null=True)
    images = MediaSerializer(allow_null=True, many=True)

    class Meta:
        model = Analyze
        fields = "__all__"

