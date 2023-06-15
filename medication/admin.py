from django.contrib import admin

from .models import HIVLabTest, ARTRegimen, PatientHivMedication, Triad


# Register your models here.

class PatientLabTestInline(admin.TabularInline):
    model = HIVLabTest


class PatientTriadInline(admin.TabularInline):
    model = Triad


class PatientPrescriptionInline(admin.TabularInline):
    model = PatientHivMedication


@admin.register(Triad)
class TriadAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'weight', 'height', 'temperature', 'heart_rate', 'blood_pressure', 'created_at')


@admin.register(HIVLabTest)
class HIVLabTestAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'cd4_count', 'viral_load')


@admin.register(ARTRegimen)
class ARTRegimenAdmin(admin.ModelAdmin):
    list_display = ('regimen_line', 'regimen', 'created_at', 'updated_at')


@admin.register(PatientHivMedication)
class PatientHivMedicationAdmin(admin.ModelAdmin):
    list_display = ("patient", 'regimen', 'is_current', 'doctor', 'created_at', 'updated_at')


class PatientHivMedicationInline(admin.TabularInline):
    model = PatientHivMedication
