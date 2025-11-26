from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer


class IdNameSerializer(Serializer):
    id = IntegerField(read_only=True)
    name = CharField()


class IdLabelSerializer(Serializer):
    id = IntegerField(read_only=True)
    label = CharField()


class SelectSerializer(Serializer):
    value = IntegerField(read_only=True, source='id')
    label = CharField(read_only=True, source='name')
