from django.conf import settings
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase

from users.models import User
from utils.pagination import CommonPagination
from utils.serializers import SelectSerializer
from users.serializers import (
    LoginSerializer, MeSerializer,
    UserListSerializer,
    UserRetrieveSerializer, UserSerializer
)
from utils.exceptions import CommonException

from utils.permissions import IsAdmin
from logs.service import AuditLogService


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['role', 'gender']
    search_fields = ('first_name', 'last_name', 'username', 'father_name')
    pagination_class = CommonPagination

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'list':
            serializer = UserListSerializer
        elif self.action == 'retrieve':
            serializer = UserRetrieveSerializer
        return serializer

    @action(
        detail=False, methods=['GET'], url_path='select',
        pagination_class=None,
        serializer_class=SelectSerializer(many=True),
    )
    def select(self, request):
        queryset = self.get_queryset().only('id', 'first_name', 'last_name').annotate(
            value=F('id'),
            label=Concat(F('first_name'), Value(' '), F('last_name'))
        ).values('value', 'label')
        return Response(queryset)

    def perform_create(self, serializer):
        serializer.save()
        AuditLogService.log(
            request=self.request,
            action="Yaratish",
            object_type="Foydalanuvchi",
            object_id=serializer.instance.id,
            description="Foydalanuvchi yaratildi"
        )

    def perform_update(self, serializer):
        serializer.save()
        AuditLogService.log(
            request=self.request,
            action="Tahrirlash",
            object_type="Foydalanuvchi",
            object_id=serializer.instance.id,
            description="Foydalanuvchi tahrirlandi"
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == User.ADMIN:
            if not request.user.is_staff:
                raise CommonException("You do not have permission to delete an admin.", HTTP_403_FORBIDDEN)

        instance.is_active = False
        instance.username = f"deleted_{instance.pk}_{get_random_string(5)}"
        instance.save(update_fields=["is_active", "username"])

        AuditLogService.log(
            request=self.request,
            action="O'chirish",
            object_type="Foydalanuvchi",
            object_id=instance.id,
            description="Foydalanuvchi o'chirildi"
        )

        return Response(status=HTTP_200_OK)


class LoginView(TokenViewBase):
    authentication_classes = []
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = serializer.validated_data
        
        AuditLogService.log(
            request=request,
            action="Login",
            object_type="Tizim",
            description=f"Foydalanuvchi tizimga kirdi: {data['user']['username']}"
        )
        
        response = Response(data=data['user'], status=HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data["access"],
            expires=(timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']).strftime(
                "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=data["refresh"],
            expires=(timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']).strftime(
                "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return response


class LogoutView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        AuditLogService.log(
            request=request,
            action="Logout",
            object_type="Tizim",
            description="Foydalanuvchi tizimdan chiqdi"
        )
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        return response


class MeView(GenericAPIView):
    serializer_class = MeSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UsernameCheckView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.params.get('username', None)
        if username:
            exists = User.objects.filter(username=username).exists()
        return Response({'available': not exists})
