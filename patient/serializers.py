from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer
from .models import Patient


class PatientListSerializer(ModelSerializer):
    full_name = CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'age', 'gender', 'created_at']


class PatientRetrieveSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name', 'last_name', 'father_name',
            'birthday', 'age', 'gender',
            'is_active',
            'created_by',
            'created_at'
        ]


class PatientCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'father_name',
            'birthday', 'gender'
        ]
        extra_kwargs = {
            "birthday": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "father_name": {"required": True}
        }


class PatientSelectSerializer(ModelSerializer):
    """For dropdown search/select usage."""
    value = IntegerField(source='id')
    label = CharField(source='get_full_name')

    class Meta:
        model = Patient
        fields = ['value', 'label']
