from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from appointments.models import AppointMent, AppointMentType
from awards.serializers import PatientProgramEnrollmentSerializer, RedemptionSerializer
from core import permisions as custom_permissions
from core.exceptions import PatientNotFoundException
from core.models import HealthFacility, FacilityType
from doctors.models import Doctor
from patients.models import Patient


class LoyaltyPointsMixin:
    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['get'],
        url_path='my-points',
        url_name='points',
        detail=False
    )
    def my_points(self, request, *args, **kwargs):
        patient = request.user.patient
        data = {
            'total': patient.total_points,
            'total_redeemed_points': patient.total_redemption_points,
            'redeem_count': patient.redemptions.all().count(),
            'redeemable_points': patient.points_balance,
            'current_program_enrolment': PatientProgramEnrollmentSerializer(
                instance=patient.current_program_enrollment,
                context={'request': request}
            ).data if patient.current_program_enrollment is not None else None,
            'redeem_list': RedemptionSerializer(
                instance=patient.redemptions.all(),
                many=True,
                context={'request': request}
            ).data
        }
        return Response(data)

    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['get'],
        url_path='points-history',
        url_name='points-history',
        detail=False
    )
    def points_history(self, request, *args, **kwargs):
        from orders.models import DeliveryFeedBack
        from .serializers import PointsHistorySerializer
        feed_back = DeliveryFeedBack.objects.filter(delivery__order__appointment__patient__user=request.user)
        queryset = self.filter_queryset(feed_back)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PointsHistorySerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PointsHistorySerializer(queryset, many=True)

        return Response(serializer.data)

    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['post'],
        url_path='redeem-points',
        url_name='redeem-points',
        detail=True,
        serializer_class=RedemptionSerializer
    )
    def redeem(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, id=kwargs['pk'], user=request.user)
        serializer = RedemptionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # TODO CHECK IF MAX REDEMPTION REACHED IN EITHER SERIALIZER validator or here
        points_redeemed = serializer.validated_data.get("reward").point_value
        instance = serializer.save(patient=patient, points_redeemed=points_redeemed)
        data = {
            'total': patient.total_points,
            'total_redeemed_points': patient.total_redemption_points,
            'redeem_count': patient.redemptions.all().count(),
            'redeemable_points': patient.points_balance,
            'program_enrolments': PatientProgramEnrollmentSerializer(
                instance=patient.enrollments,
                many=True,
                context={'request': request}
            ).data,
            'current_program_enrolment': PatientProgramEnrollmentSerializer(
                instance=patient.current_program_enrollment,
                context={'request': request}
            ).data if patient.current_program_enrollment is not None else None,
            'redemption': RedemptionSerializer(instance=instance, context={'request': request}).data
        }
        return Response(data)


class PatientAppointmentSyncMixin:
    def update_or_create_appointments(self, appointments_dict, patient_instance):
        if appointments_dict["count"] == 0:
            return
        for appointment in appointments_dict["list"]:
            try:
                appointment_instance = AppointMent.objects.get(remote_id=appointment["id"])
                # TODO perform update
            except AppointMent.DoesNotExist:
                appointment_instance = AppointMent.objects.create(
                    remote_id=appointment["id"],
                    patient=patient_instance,
                    type=self.get_or_create_appointment_type(appointment["type"]),
                    doctor=self.get_or_create_doctor(appointment["doctor"]),
                    next_appointment_date=appointment["next_appointment_date"]
                )

    def get_or_create_appointment_type(self, appointment_type_dict):
        try:
            appointment_typ = AppointMentType.objects.get(remote_id=appointment_type_dict["id"])
        except AppointMentType.DoesNotExist:
            appointment_typ = AppointMentType.objects.create(
                remote_id=appointment_type_dict["id"],
                type=appointment_type_dict["type"],
                description=appointment_type_dict["description"],
            )
        return appointment_typ

    def get_or_create_doctor(self, doctor_dict):
        """
        Checks of doctor exist else it creates a user and associates it with doctor
        """
        try:
            doctor = Doctor.objects.get(doctor_number=doctor_dict["doctor_number"])
        except Doctor.DoesNotExist:
            import secrets
            user = User.objects.create_user(
                username=doctor_dict["email"],
                email=doctor_dict["email"],
                password=secrets.token_hex(6),
                first_name=doctor_dict["first_name"],
                last_name=doctor_dict["last_name"]
            )
            profile = user.profile
            profile.user_type = 'doctor'
            doctor = Doctor.objects.create(
                user=user,
                doctor_number=doctor_dict["doctor_number"]
            )
        return doctor


class FacilitySyncMixin:
    def update_or_create_facilities(self, facilities_dict):
        if facilities_dict["count"] == 0 or \
                HealthFacility.objects.all().count() == facilities_dict["count"]:
            return
        for facility in facilities_dict["results"]:
            self.get_or_create_facility(facility)

    def get_or_create_facility(self, facility_dict):
        facility = None
        try:
            facility = HealthFacility.objects.get(identification_code=facility_dict["identification_code"])
            # TODO update facility
        except HealthFacility.DoesNotExist:
            facility_type = self.get_or_create_facility_type(facility_dict["type"])
            facility = HealthFacility.objects.create(
                identification_code=facility_dict["identification_code"],
                name=facility_dict["name"],
                type=facility_type,
                longitude=facility_dict["longitude"],
                latitude=facility_dict["latitude"],
                address=facility_dict["address"]
            )
        return facility

    def get_or_create_facility_type(self, facility_type_dict):
        facility_type = None
        try:
            facility_type = FacilityType.objects.get(remote_id=facility_type_dict["id"])
            # TODO update facility type
        except FacilityType.DoesNotExist:
            facility_type = FacilityType.objects.create(
                remote_id=facility_type_dict["id"],
                level=facility_type_dict["level"],
                name=facility_type_dict["name"],
                description=facility_type_dict["description"]
            )
        return facility_type


class PatientSyncMixin:
    def get_or_create_patient(self, uuid: str):
        from users.api import get_patient_by_uuid
        try:
            # get patient
            patient = Patient.objects.get(uuid=uuid)
        except Patient.DoesNotExist:
            # create_patient
            remote_patient = get_patient_by_uuid(uuid)
            if remote_patient is not None:
                patient = self.create_patient(remote_patient)
            else:
                raise PatientNotFoundException()
        return patient

    def create_patient(self, remote_patient: dict):
        # TODO Create patient from remote data and return the object
        patient = Patient.objects.create(
            uuid=remote_patient['uuid'],
            patient_number=self.get_ccc_number(remote_patient['person']['identifiers']),
            national_id=self.get_national_id(remote_patient['person']['identifiers']),
            date_of_birth=remote_patient['person']['birthdate'],
            marital_status=None,
            base_clinic=None,
            refill_scheme=None,
            county_of_residence=None,
            occupation=None,
            first_name=remote_patient['person']['preferredName']['givenName'],
            last_name=remote_patient['person']['preferredName']['middleName'],
            surname=remote_patient['person']['preferredName']['familyName'],
            phone_number=self.get_phone_number(remote_patient['person']['attributes'])
        )

        # TODO GET APPOINTMENTS, TRIAGE AND LAB RESULTS TOGETHER WITH ORDERS

        return patient

    def get_ccc_number(self, identifiers: list):
        pass

    def get_national_id(self, identifiers: list):
        pass

    def get_phone_number(self, attributes: list):
        pass
