from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnalyzePredictAPIView, AnalyzeViewSet

router = DefaultRouter(trailing_slash=False)
router.register("analyzes", AnalyzeViewSet, basename="analyzes")

urlpatterns = [
    path('predict', AnalyzePredictAPIView.as_view()),

    path('', include(router.urls))
]