from django.contrib import admin

from awards.admin import PatientRedemptionInline, PatientProgramEnrollmentInline
from awards.models import PatientProgramEnrollment
from core.admin import TransferRequestInline
from .models import PatientNextOfKeen, Patient
from appointments.admin import AppointMentInline
from medication.admin import PatientPrescriptionInline
# Register your models here.


@admin.register(PatientProgramEnrollment)
class PatientProgramEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'program', 'is_current', 'created_at', 'updated_at')


class PatientNextOfKeenInline(admin.TabularInline):
    model = PatientNextOfKeen


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", 'patient_number', 'base_clinic', 'created_at')
    inlines = [
        PatientPrescriptionInline,
        PatientProgramEnrollmentInline,
        PatientNextOfKeenInline,
        AppointMentInline,
        PatientRedemptionInline,
        TransferRequestInline,
    ]

