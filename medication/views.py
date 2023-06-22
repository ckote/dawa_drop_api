from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from core import permisions as custom_permissions
from .models import HIVLabTest, ARTRegimen, PatientHivMedication, Triad
from .serializers import (
    HIVLabTestSerializer,
    ARTRegimenSerializer, PatientHivMedicationSerializer,
    TriadSerializer
)


# Create your views here.


class HIVLabTestViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = HIVLabTest.objects.all()
    serializer_class = HIVLabTestSerializer


class PatientHIVLabTestViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPatient,
        custom_permissions.HasRelatedUserType
    ]
    serializer_class = HIVLabTestSerializer

    def get_queryset(self):
        patient = self.request.user.patient
        queryset = HIVLabTest.objects.filter(appointment__patient=patient)
        return queryset


class ARTRegimenViewSet(viewsets.ModelViewSet):
    queryset = ARTRegimen.objects.all()
    serializer_class = ARTRegimenSerializer


class PatientHivMedicationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPatient
    ]

    serializer_class = PatientHivMedicationSerializer

    def get_queryset(self):
        patient = self.request.user.patient
        queryset = patient.prescriptions.all()
        return queryset


class TriadViewSet(viewsets.ModelViewSet):
    serializer_class = TriadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Triad.objects.filter(appointment__patient__user=self.request.user)

