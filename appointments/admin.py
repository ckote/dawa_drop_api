from django.contrib import admin

from .models import AppointMentType, AppointMent
from medication.admin import PatientTriadInline, PatientLabTestInline


# Register your models here.


@admin.register(AppointMentType)
class AppointMentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'description', 'created_at')


class AppointMentInline(admin.TabularInline):
    model = AppointMent


@admin.register(AppointMent)
class AppointMentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'type', 'doctor', 'next_appointment_date', 'created_at', 'updated_at')
    inlines = [
        PatientTriadInline, PatientLabTestInline
    ]
