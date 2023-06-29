from django.contrib.auth.models import User
from appointments import api
from appointments.models import AppointMent, AppointMentType
from doctors.models import Doctor
from patients.mixins.sync import PatientSyncMixin


class PatientAppointmentSyncMixin(PatientSyncMixin):
    """
    If no patient then there is need to create one hence extending the Patient sync mixin
    """

    def get_or_create_appointment(self, encounter, patient=None):
        """Gets appointment from the database if it exist else creates an appointment from
        encounter
        """
        try:
            appointment_instance = AppointMent.objects.get(uuid=encounter["uuid"])
        except AppointMent.DoesNotExist:
            appointment_instance = AppointMent.objects.create(
                uuid=encounter["uuid"],
                patient=self.get_or_create_patient(encounter["patient"]["uuid"]) if patient is None else patient,
                type=self.get_or_create_appointment_type(encounter["encounterType"]),
                doctor=self.get_or_create_doctor(encounter["encounterProviders"]),
                scheduled_time=encounter["encounterDatetime"],
                next_appointment_date=encounter["next_appointment_date"]
            )
        return appointment_instance

    @staticmethod
    def get_remote_type(uuid):
        return api.get_remote_type(uuid)

    def get_or_create_appointment_type(self, encounter_type):
        """Gets appointment type from db if existe else creates one using wncounter dictionary and return it
        @param encounter_type: EMR encounter type dictionary
        @return: AppointMentType
        """
        try:
            appointment_typ = AppointMentType.objects.get(
                uuid=encounter_type["uuid"])
        except AppointMentType.DoesNotExist:

            appointment_typ = AppointMentType.objects.create(
                uuid=encounter_type["uuid"],
                type=encounter_type["name"],
                description=encounter_type["description"],
            )
        return appointment_typ

    def get_or_create_doctor(self, encounter_providers):
        """
        Checks of doctor exist else it creates a user and associates it with doctor
        """
        # TODO Implement fully
        try:
            doctor = Doctor.objects.get(doctor_number=encounter_providers["doctor_number"])
        except Doctor.DoesNotExist:
            import secrets
            user = User.objects.create_user(
                username=encounter_providers["email"],
                email=encounter_providers["email"],
                password=secrets.token_hex(6),
                first_name=encounter_providers["first_name"],
                last_name=encounter_providers["last_name"]
            )
            profile = user.profile
            profile.user_type = 'doctor'
            doctor = Doctor.objects.create(
                user=user,
                doctor_number=encounter_providers["doctor_number"]
            )
        return doctor
