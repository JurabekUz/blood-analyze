from django.urls import path, include
from rest_framework import routers

from users.views import (
    MeView, LoginView, LogoutView, UsernameCheckView, UserViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/login', LoginView.as_view()),
    path('auth/logout', LogoutView.as_view()),
    path('auth/checking', UsernameCheckView.as_view()),

    path('users/me', MeView.as_view()),

    path('', include(router.urls)),
]
