from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core import permisions as custom_permissions
from .filterset import AppointMentFilterSet
from .models import AppointMentType
from .serializers import AppointMentTypeSerializer, AppointMentSerializer
from rest_framework import views

# Create your views here.


class AppointMentTypeViewSet(viewsets.ModelViewSet):
    queryset = AppointMentType.objects.all()
    serializer_class = AppointMentTypeSerializer


class AppointMentViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPatient,
        custom_permissions.HasRelatedUserType
    ]
    search_fields = (
        "doctor__user__first_name", "doctor__user__last_name",
        "doctor__user__profile__phone_number", "doctor__doctor_number"
    )
    def get_queryset(self):
        return self.request.user.patient.appointments.all()

    def list(self, request, *args, **kwargs):
        from .api import get_appointments
        from users.api import get_user_id
        user_id = get_user_id("0712311264", '11111111')['user_id']
        print(user_id)
        remote_appointments = get_appointments(user_id)
        return Response(remote_appointments)