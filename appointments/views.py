from django.shortcuts import render
from rest_framework import viewsets, permissions
from core import permisions as custom_permissions
from .filterset import AppointMentFilterSet
from .models import AppointMentType
from .serializers import AppointMentTypeSerializer, AppointMentSerializer


# Create your views here.


class AppointMentTypeViewSet(viewsets.ModelViewSet):
    queryset = AppointMentType.objects.all()
    serializer_class = AppointMentTypeSerializer


class AppointMentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPatient,
        custom_permissions.HasRelatedUserType
    ]
    serializer_class = AppointMentSerializer
    filterset_class = AppointMentFilterSet

    search_fields = (
        "doctor__user__first_name", "doctor__user__last_name",
        "doctor__user__profile__phone_number", "doctor__doctor_number"
    )

    def get_queryset(self):
        return self.request.user.patient.appointments.all()
