from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core import permisions as custom_permissions
from patients.api import get_and_sync_appointments, get_prescriptions, get_triads, get_tests, \
    get_patient_summary_statistics
from patients.mixins.views import LoyaltyPointsMixin
from patients.models import Patient, PatientNextOfKeen
from patients.serializers import PatientSerializer, PatientNextOfKeenSerializer


# Create your views here.

class PatientViewSet(viewsets.ModelViewSet, LoyaltyPointsMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientNextOfKeenViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPatientOrReadOnly,
        custom_permissions.HasRelatedUserType
    ]
    serializer_class = PatientNextOfKeenSerializer

    def perform_create(self, serializer):
        patient = get_object_or_404(Patient, id=self.kwargs['patient_pk'], user=self.request.user)
        serializer.save(patient=patient)

    def get_queryset(self):
        if self.request.user.profile.user_type == 'doctor':
            return PatientNextOfKeen.objects.all()
        curr_patient = self.request.user.patient
        patient = get_object_or_404(Patient, id=self.kwargs['patient_pk'])
        if curr_patient != patient:
            raise PermissionDenied(
                detail="Warning!!Your are forbidden from accessing other patient private information",
            )
        return PatientNextOfKeen.objects.filter(patient=patient)
