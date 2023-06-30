from appointments import api
from appointments.models import AppointMent, AppointMentType
from doctors.mixins.sync import ProviderSyncMixin

from patients.mixins.sync import PatientSyncMixin


class PatientAppointmentSyncMixin(PatientSyncMixin, ProviderSyncMixin):
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
                doctor=self.get_or_create_doctor_from_encounter_providers(encounter["encounterProviders"]),
                scheduled_time=encounter["encounterDatetime"],
                # TODO Handle the next appointment date please
                # next_appointment_date=encounter["next_appointment_date"]
            )
        return appointment_instance

    @staticmethod
    def get_remote_type(uuid):
        return api.get_encounter_type(uuid)

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

    def sync_appointments(self, patient):
        from appointments.api import get_patient_encounters
        encounters = get_patient_encounters(patient.uuid)
        for encounter in encounters:
            self.get_or_create_appointment(encounter, patient)

    def get_remote_encounter_types(self):
        return api.get_encounter_types()
