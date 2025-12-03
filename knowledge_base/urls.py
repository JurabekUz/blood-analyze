from django.urls import path, include
from rest_framework import routers

from .views import MediaCreateView, DiseaseViewSet, MediaDeleteView

router = routers.DefaultRouter(trailing_slash=False)
router.register('diseases', DiseaseViewSet)


urlpatterns = [
    path('media', MediaCreateView.as_view()),
    path('media/<int:pk>', MediaDeleteView.as_view()),

    path('', include(router.urls))
]