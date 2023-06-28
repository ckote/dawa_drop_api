from django.db import models


# Create your models here.


class AppointMentType(models.Model):
    uuid = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['-created_at']


class AppointMent(models.Model):
    uuid = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    patient = models.ForeignKey("patients.Patient", related_name='appointments', on_delete=models.CASCADE)
    type = models.ForeignKey('appointments.AppointMentType', related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', related_name='appointments', on_delete=models.CASCADE, )
    next_appointment_date = models.DateField(null=True, blank=True)
    start_date_time = models.DateTimeField(null=True, blank=True)
    stop_date_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.patient_number} {self.type} appointment"

    class Meta:
        ordering = ['-created_at']
