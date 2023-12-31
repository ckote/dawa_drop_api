from django.contrib import admin

from core.models import HealthFacility, DeliveryMode, FacilityTransferRequest, FacilityType, MaritalStatus, \
    DeliveryTimeSlot, RefillScheme


# Register your models here.


@admin.register(HealthFacility)
class HIVClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude', 'address')


@admin.register(DeliveryMode)
class DeliveryModeAdmin(admin.ModelAdmin):
    list_display = ('mode',)


@admin.register(FacilityTransferRequest)
class TransferRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'hospital', 'reason',
        'is_approved', 'approved_by', 'created_at',
        'updated_at'
    )


class TransferRequestInline(admin.TabularInline):
    model = FacilityTransferRequest


@admin.register(FacilityType)
class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ('level', 'name')


@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'description', 'is_active', 'created_at')


@admin.register(DeliveryTimeSlot)
class DeliveryTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('slot', 'start', 'end', 'description')


@admin.register(RefillScheme)
class RefillSchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'time', 'units', 'is_default')
    list_editable = ['is_default', 'units', 'time']
