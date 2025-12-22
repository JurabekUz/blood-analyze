from datetime import date

from django.db.models.functions import ExtractMonth
from django.utils import timezone

from django.db.models import Count, Avg, Exists, OuterRef, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response

from .filters import get_week_range, get_month_range, get_year_range

from patient.models import Patient
from .models import Analyze


def build_statistics(start, end):
    base_filter = {
        "created_at__date__gte": start,
        "created_at__date__lte": end,
    }

    results = {}

    results["total_analyzes"] = Analyze.objects.filter(**base_filter).count()

    results["analyzes_by_disease"] = list(
        Analyze.objects
        .filter(**base_filter)
        .values("disease__id", "disease__name")
        .annotate(count=Count("id"))
    )

    results["total_patients"] = (
        Patient.objects.filter(
            analyzes__created_at__date__range=(start, end),
            is_active=True
        )
        .distinct()
        .count()
    )

    results["analyzes_by_doctors"] = list(
        Analyze.objects
        .filter(**base_filter)
        .values("user__id", "user__first_name", "user__last_name")
        .annotate(count=Count("id"))
    )

    results["patients_by_gender"] = list(
        Patient.objects.filter(
            analyzes__created_at__date__range=(start, end),
            is_active=True,
        )
        .values("gender")
        .annotate(
            count=Count("id", distinct=True)
        )
        .order_by("gender")
    )

    results["avg_accuracy"] = (
        Analyze.objects
        .filter(**base_filter, accuracy__isnull=False)
        .aggregate(avg=Avg("accuracy"))
    )["avg"]

    return results


class StatsByDateAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("date", OpenApiTypes.DATE),
        ],
    )
    def get(self, request):
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"error": "date is required"}, status=400)

        target = date.fromisoformat(date_str)
        stats = build_statistics(target, target)
        return Response(stats)


class StatsByWeekAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("week", OpenApiTypes.INT),
        ],
    )
    def get(self, request):
        year = timezone.now().year
        week = int(request.query_params.get("week"))

        start, end = get_week_range(year, week)
        stats = build_statistics(start, end)
        return Response(stats)


class StatsByMonthAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("month", OpenApiTypes.INT),
        ],
    )
    def get(self, request):
        year = timezone.now().year
        month = int(request.query_params.get("month"))

        start, end = get_month_range(year, month)
        stats = build_statistics(start, end)
        return Response(stats)


class StatsByYearAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("year", OpenApiTypes.INT),
        ],
    )
    def get(self, request):
        year = int(request.query_params.get("year"))
        start, end = get_year_range(year)

        stats = build_statistics(start, end)
        return Response(stats)


class MonthlyPatientsByGenderAPIView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter("year", OpenApiTypes.INT),
        ]
    )
    def get(self, request):
        year = int(request.query_params.get("year"))

        qs = (
            Analyze.objects
            .filter(created_at__year=year)
            .values(
                month=ExtractMonth("created_at"),
                gender=F("patient__gender")
            )
            .annotate(
                patient_count=Count("patient_id", distinct=True)
            )
        )

        # Prepare empty structure
        result = {
            "labels": list(range(1, 13)),
            "series": {
                "male": [0] * 12,
                "female": [0] * 12,
            }
        }

        for row in qs:
            idx = row["month"] - 1
            if row["gender"] == Patient.MALE:
                result["series"]["male"][idx] = row["patient_count"]
            elif row["gender"] == Patient.FEMALE:
                result["series"]["female"][idx] = row["patient_count"]

        return Response(result)


class MonthlyAnalyzeAndPatientCountAPIView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter("year", OpenApiTypes.INT),
        ]
    )
    def get(self, request):
        year = int(request.query_params.get("year"))

        qs = (
            Analyze.objects
            .filter(created_at__year=year)
            .values(month=ExtractMonth("created_at"))
            .annotate(
                analyze_count=Count("id"),
                patient_count=Count("patient_id", distinct=True)
            )
        )

        result = {
            "labels": list(range(1, 13)),
            "series": {
                "analyzes": [0] * 12,
                "patients": [0] * 12,
            }
        }

        for row in qs:
            idx = row["month"] - 1
            result["series"]["analyzes"][idx] = row["analyze_count"]
            result["series"]["patients"][idx] = row["patient_count"]

        return Response(result)


