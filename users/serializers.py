from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = MeSerializer(self.user).data
        return data


class MeSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'father_name', 'role')


class UserListSerializer(ModelSerializer):
    full_name = SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username',
            'first_name', 'last_name', 'father_name',
            'role', 'gender', 'birthday',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class UserRetrieveSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username',
            'first_name', 'last_name', 'father_name',
            'role', 'age', 'gender', 'birthday', 'date_joined'
        )


class UserFullNameSerializer(ModelSerializer):
    full_name = SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()


class UsernameCheckSerializer(Serializer):
    username = CharField(max_length=150, required=True)

