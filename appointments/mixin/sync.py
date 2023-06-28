from django.contrib.auth.models import User
from appointments import api
from appointments.models import AppointMent, AppointMentType
from doctors.models import Doctor


class PatientAppointmentSyncMixin:
    def get_or_create_appointment(self, appointment, patient_instance):
        try:
            appointment_instance = AppointMent.objects.get(uuid=appointment["uuid"])
        except AppointMent.DoesNotExist:
            appointment_instance = AppointMent.objects.create(
                uuid=appointment["uuid"],
                patient=self.get_or_create_patient(appointment["patient"]["uuid"]),
                type=self.get_or_create_appointment_type(appointment["visitType"], False),
                start_date_time=appointment["startDatetime"],
                stop_date_time=appointment["stopDatetime"],
                # TODO study encounter provider to know if its same as the doctor or not
                doctor=self.get_or_create_doctor(appointment["doctor"]),
                next_appointment_date=appointment["next_appointment_date"]
            )
        return appointment_instance

    def get_or_create_patient(self, uuid):
        # TODO fetch patient with uuid and add to patient module
        from patients.models import Patient
        return Patient.objects.get(uuid=uuid)

    @staticmethod
    def get_remote_type(uuid):
        return api.get_remote_type(uuid)

    def get_or_create_appointment_type(self, appointment_type, is_detailed):
        try:
            appointment_typ = AppointMentType.objects.get(
                uuid=appointment_type["uuid"])
        except AppointMentType.DoesNotExist:
            type_ = None
            if is_detailed:
                type_ = appointment_type
            else:
                type_ = self.get_remote_type(appointment_type["uuid"])
            appointment_typ = AppointMentType.objects.create(
                uuid=type_["uuid"],
                type=type_["name"],
                description=type_["description"],
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
