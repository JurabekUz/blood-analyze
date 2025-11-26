from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

router = DefaultRouter(trailing_slash=False)
router.register("patients", PatientViewSet, basename="patients")

urlpatterns = [
    path('', include(router.urls))
]
