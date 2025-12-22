from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnalyzePredictAPIView, AnalyzeViewSet

router = DefaultRouter(trailing_slash=False)
router.register("analyzes", AnalyzeViewSet, basename="analyzes")

urlpatterns = [
    path('predict', AnalyzePredictAPIView.as_view()),

    path('', include(router.urls))
]

from .stat import (
    StatsByDateAPIView,
    StatsByWeekAPIView,
    StatsByMonthAPIView,
    StatsByYearAPIView,
    MonthlyAnalyzeAndPatientCountAPIView,
    MonthlyPatientsByGenderAPIView
)

urlpatterns += [
    path("statistics/date", StatsByDateAPIView.as_view()),
    path("statistics/week", StatsByWeekAPIView.as_view()),
    path("statistics/month", StatsByMonthAPIView.as_view()),
    path("statistics/year", StatsByYearAPIView.as_view()),
    path("statistics/analyzes-vs-patients/monthly", MonthlyAnalyzeAndPatientCountAPIView.as_view()),
    path("statistics/patients-by-gender/monthly", MonthlyPatientsByGenderAPIView.as_view()),
]
