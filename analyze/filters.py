import django_filters

from .models import Analyze


class PatientFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="created_at__date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at__date", lookup_expr="lte")

    class Meta:
        model = Analyze
        fields = [
            'user',
            'patient',
            'disease'
        ]


from datetime import date, timedelta


def get_week_range(year: int, week: int):
    # ISO week format
    first_day = date.fromisocalendar(year, week, 1)
    last_day = first_day + timedelta(days=6)
    return first_day, last_day


def get_month_range(year: int, month: int):
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year, 12, 31)
    else:
        next_month = date(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
    return first_day, last_day


def get_year_range(year: int):
    return date(year, 1, 1), date(year, 12, 31)
