from django.db import models
from django.utils import timezone


# Create your models here.


class HIVLabTest(models.Model):
    remote_id = models.PositiveIntegerField(unique=True)
    appointment = models.ForeignKey("appointments.AppointMent", related_name='lab_tests', on_delete=models.CASCADE)
    cd4_count = models.PositiveIntegerField()
    viral_load = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.appointment.patient} lab HIV test"

    class Meta:
        ordering = ['-appointment__created_at']


class ARTRegimen(models.Model):
    remote_id = models.PositiveIntegerField(unique=True)
    regimen_line = models.CharField(max_length=50, unique=True)
    regimen = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.regimen

    class Meta:
        ordering = ['-created_at']


class PatientHivMedication(models.Model):
    """
    HIV prescription
    """
    remote_id = models.PositiveIntegerField(unique=True)
    patient = models.ForeignKey('patients.Patient', related_name='prescriptions', on_delete=models.CASCADE)
    regimen = models.ForeignKey(ARTRegimen, related_name='prescriptions', on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)
    doctor = models.ForeignKey("doctors.Doctor", related_name='prescriptions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} {self.regimen}"

    class Meta:
        ordering = ['-created_at']


class Triad(models.Model):
    appointment = models.ForeignKey('appointments.AppointMent', on_delete=models.CASCADE, related_name='triads')
    weight = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    height = models.DecimalField(decimal_places=2, max_digits=12)
    temperature = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
