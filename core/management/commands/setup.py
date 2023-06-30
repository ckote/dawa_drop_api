from django.core.management.base import BaseCommand
from appointments.models import AppointMentType
from appointments.mixin.sync import PatientAppointmentSyncMixin


class Command(BaseCommand, PatientAppointmentSyncMixin):
    help = 'Import Excel data into the database'
    headers = []

    def sync_appointment_types(self):
        encounter_types = self.get_remote_encounter_types()
        for encounter_type in encounter_types:
            appointment_type = self.get_or_create_appointment_type(encounter_type)
            self.stdout.write(self.style.SUCCESS(f'[✔]Appointment type "{appointment_type.type}" imported successfully!.'))

    def handle(self, *args, **options):
        self.sync_appointment_types()
        self.stdout.write(self.style.SUCCESS('[✔]Appointment types imported successfully!.'))
