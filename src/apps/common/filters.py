from django.utils import timezone
from django_filters.rest_framework import DateFilter, FilterSet


class BaseFilter(FilterSet):
    begin_date = DateFilter(field_name="created_at", lookup_expr="date__gte")
    end_date = DateFilter(field_name="created_at", lookup_expr="date__lte")


def beginning_of_the_current_month():
    return timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
