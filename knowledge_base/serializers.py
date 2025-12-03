from rest_framework.serializers import ModelSerializer, Serializer, ListField, ImageField, SerializerMethodField
from .models import Disease, Media


class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        exclude = ['is_active']


class DiseaseListSerializer(ModelSerializer):
    short_description = SerializerMethodField()

    class Meta:
        model = Disease
        fields = ['id', 'name', 'short_description']

    def get_short_description(self, obj):
        return obj.description[:100] + "..."


class DiseaseCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = ["id", "name", "description"]



class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "name", "file"]


class MultipleMediaCreateSerializer(Serializer):
    files = ListField(
        child=ImageField(), allow_empty=False
    )

    def create(self, validated_data):
        files = validated_data["files"]
        medias = [Media.objects.create(file=f) for f in files]
        return medias

    def to_representation(self, instance):
        return MediaSerializer(instance, many=True).data




