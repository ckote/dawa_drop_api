from doctors.models import Doctor
from django.contrib.auth.models import User


class ProviderSyncMixin:
    @staticmethod
    def get_remote_provider(uuid):
        from doctors.api import get_provider
        return get_provider(uuid)

    def get_or_create_doctor(self, provider):
        """
        Checks of doctor exist else it creates a user and associates it with doctor
        """
        try:
            doctor = Doctor.objects.get(uuid=provider['uuid'])
        except Doctor.DoesNotExist:
            doctor = Doctor.objects.create(
                uuid=provider['uuid'],
            )
        return doctor

    def get_or_create_doctor_from_encounter_providers(self, encounter_providers: list):
        if encounter_providers:
            provider_uuid = encounter_providers[0]['provider']['uuid']
            remote_provider = self.get_remote_provider(provider_uuid)
            return self.get_or_create_doctor(remote_provider)
