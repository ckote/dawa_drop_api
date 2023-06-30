from django.contrib import admin

from .models import AppointMentType, AppointMent
from medication.admin import PatientTriadInline, PatientLabTestInline


# Register your models here.


@admin.register(AppointMentType)
class AppointMentTypeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'type', 'preferred', 'description', 'created_at')
    search_fields = ('uuid', 'type', 'description', 'created_at')
    list_filter = ('uuid', 'type', 'description', 'created_at')
    list_editable = ("preferred",)


class AppointMentInline(admin.TabularInline):
    model = AppointMent


@admin.register(AppointMent)
class AppointMentAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'patient', 'type', 'doctor',
        'next_appointment_date', 'created_at', 'updated_at'
    )
    list_filter = (
        'uuid', 'patient', 'type', 'doctor',
        'next_appointment_date', 'created_at', 'updated_at'
    )
    search_fields = (
        'uuid', 'patient', 'type', 'doctor',
        'next_appointment_date', 'created_at', 'updated_at'
    )
    inlines = [
        PatientTriadInline, PatientLabTestInline
    ]
