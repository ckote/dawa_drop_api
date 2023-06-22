from django_filters.rest_framework import filterset, filters

from .models import HIVLabTest, Triad


class LabResultFilterSet(filterset.FilterSet):
    year = filters.NumberFilter(field_name='appointment', lookup_expr='created_at__year', label="Appointment year")

    class Meta:
        model = HIVLabTest
        fields = ()


class TriadFilterSet(filterset.FilterSet):
    year = filters.NumberFilter(field_name='appointment', lookup_expr='created_at__year', label="Appointment year")

    class Meta:
        model = Triad
        fields = ()
