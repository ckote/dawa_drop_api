from rest_framework import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions

from users.models import Patient
from . import permisions as custom_permissions
from .models import HealthFacility, DeliveryMode, FacilityTransferRequest, FacilityType, MaritalStatus, \
    DeliveryTimeSlot
from .serializers import HealthFacilitySerializer, DeliveryModeSerializer, TransferRequestSerializer, \
    FacilityTypeSerializer, MaritalStatusSerializer, DeliveryTimeSlotSerializer, EMRPatientNotificationSerializer
from . import mixin


# Create your views here.


class ApiRootView(APIView):
    def get(self, request):
        return Response({
            "users_url": reverse.reverse_lazy('users:user-list', request=request),
            "doctors_url": reverse.reverse_lazy('doctors:doctor-list', request=request),
            # "doctors_url": reverse.reverse_lazy('users:user-doctor-list', request=request),
            "deliver_agents_url": reverse.reverse_lazy('agents:agent-list', request=request),
            "marital_status": reverse.reverse_lazy('core:marital-status-list', request=request),
            "appointment_types": reverse.reverse_lazy('appointments:type-list', request=request),
            "appointments": reverse.reverse_lazy('appointments:appointment-list', request=request),
            # "deliver_agents_url": reverse.reverse_lazy('users:user-agent-list', request=request),
            "patients_url": reverse.reverse_lazy('patients:patient-list', request=request),
            "patients_transfer_request_url": reverse.reverse_lazy('core:transfer-request-list', request=request),
            "enrollments_url": reverse.reverse_lazy('awards:enrollment-list', request=request),
            # "patient_appointments": reverse.reverse_lazy('patients:appointment-list', request=request),
            "patient_prescriptions": reverse.reverse_lazy('medications:patient-hiv-prescription-list', request=request),
            "patient_triads": reverse.reverse_lazy('medications:triad-list', request=request),
            "patient_test_results": reverse.reverse_lazy('medications:lab-test-list', request=request),
            # "patients_url": reverse.reverse_lazy('users:user-patient-list', request=request),
            "health_facilities_types": reverse.reverse_lazy('core:facility-type-list', request=request),
            "health facilities url": reverse.reverse_lazy('core:facility-list', request=request),
            "award_programs_url": reverse.reverse_lazy('awards:program-list', request=request),
            "reward_url": reverse.reverse_lazy('awards:reward-list', request=request),
            "delivery_modes_url": reverse.reverse_lazy('core:mode-list', request=request),
            "orders_url": reverse.reverse_lazy('orders:order-list', request=request),
            "feedback_url": reverse.reverse_lazy('orders:feedback-list', request=request),
            "delivery_url": reverse.reverse_lazy('orders:delivery-request-list', request=request),
        })


class HealthFacilityViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.AllowAny,
        custom_permissions.IsDoctorOrReadOnly
    ]
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer


class HealthFacilityTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.AllowAny,
        custom_permissions.IsDoctorOrReadOnly
    ]
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class DeliveryModeViewSet(viewsets.ModelViewSet):
    permission_classes = [
        custom_permissions.IsAdminOrReadOnly
    ]
    queryset = DeliveryMode.objects.all()
    serializer_class = DeliveryModeSerializer


class TransferRequestViewSet(viewsets.ModelViewSet, mixin.PatientTransferMixin):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsDoctorOrReadOnly
    ]
    queryset = FacilityTransferRequest.objects.all()
    serializer_class = TransferRequestSerializer


class MaritalStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsDoctorOrReadOnly
    ]
    queryset = MaritalStatus.objects.all()
    serializer_class = MaritalStatusSerializer


class DeliveryTimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [
        custom_permissions.IsDoctorOrReadOnly
    ]
    queryset = DeliveryTimeSlot.objects.all()
    serializer_class = DeliveryTimeSlotSerializer


class ReceiveNotificationView(APIView):
    permission_classes = [
        permissions.IsAdminUser
    ]
    queryset = Patient.objects.all()
    serializer_class = EMRPatientNotificationSerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data)
        self.create_or_update(request.data)
        return Response({"detail": "Success"})

    def perform_create(self, validated_data):
        Patient.objects.create(
            patient_number=validated_data["PATIENT_IDENTIFICATION"]["INTERNAL_PATIENT_ID"]["ID"],
            national_id=validated_data['']
        )

    def perform_update(self, instance, validated_data):
        pass

    def create_or_update(self, validated_data):
        patient_id = validated_data["PATIENT_IDENTIFICATION"]["INTERNAL_PATIENT_ID"]["ID"]
        patients = Patient.objects.filter(patient_number=patient_id)
        if patients.exists():
            self.perform_update(patients.first(), validated_data)
        else:
            self.perform_create(validated_data)
