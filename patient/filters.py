import django_filters
from django.db.models import F, ExpressionWrapper, IntegerField
from datetime import date

from .models import Patient


class PatientFilter(django_filters.FilterSet):
    # Direct fields
    gender = django_filters.CharFilter(field_name="gender", lookup_expr="exact")
    birthday = django_filters.DateFilter(field_name="birthday", lookup_expr="exact")
    birthday_from = django_filters.DateFilter(field_name="birthday", lookup_expr="gte")
    birthday_to = django_filters.DateFilter(field_name="birthday", lookup_expr="lte")

    # Age filters (computed on the fly from birthday)
    age = django_filters.NumberFilter(method="filter_age_exact")
    age_from = django_filters.NumberFilter(method="filter_age_from")
    age_to = django_filters.NumberFilter(method="filter_age_to")

    class Meta:
        model = Patient
        fields = [
            'gender',
            'birthday',
            'birthday_from',
            'birthday_to',
            'age',
            'age_from',
            'age_to',
        ]

    # Utility to compute age expression
    @staticmethod
    def _age_expression():
        """
        Compute age in SQL: (today.year - birthday.year) - (today < birthday_this_year)
        """
        today = date.today()

        return ExpressionWrapper(
            today.year
            - F("birthday__year")
            - django_filters.filters.Case(
                django_filters.filters.When(
                    birthday__month__gt=today.month,
                    then=1
                ),
                django_filters.filters.When(
                    birthday__month=today.month,
                    birthday__day__gt=today.day,
                    then=1
                ),
                default=0,
            ),
            output_field=IntegerField(),
        )

    def filter_age_exact(self, queryset, name, value):
        return queryset.annotate(age_sql=self._age_expression()).filter(age_sql=value)

    def filter_age_from(self, queryset, name, value):
        return queryset.annotate(age_sql=self._age_expression()).filter(age_sql__gte=value)

    def filter_age_to(self, queryset, name, value):
        return queryset.annotate(age_sql=self._age_expression()).filter(age_sql__lte=value)
