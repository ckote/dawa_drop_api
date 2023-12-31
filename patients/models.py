from django.db import models
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField

from awards.models import LoyaltyProgram, PatientProgramEnrollment

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)


# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='patient', null=True, blank=True)
    uuid = models.CharField(
        max_length=256, null=True, blank=True, unique=True,
        db_index=True, help_text='remote Universally unique Identifier'
    )
    patient_number = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text='Patient CCC Number')
    national_id = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.ForeignKey(
        "core.MaritalStatus", on_delete=models.CASCADE,
        related_name='patients', null=True, blank=True
    )
    # TODO handle the cascade wisely
    base_clinic = models.ForeignKey(
        "core.HealthFacility", on_delete=models.CASCADE,
        null=True, blank=True, related_name='patients'
    )
    refill_scheme = models.ForeignKey(
        "core.RefillScheme", on_delete=models.CASCADE, null=True, blank=True
    )
    county_of_residence = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=14)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def current_prescription(self):
        prescriptions = self.prescriptions.filter(is_current=True)
        return prescriptions.first() if prescriptions.exists() else None

    @property
    def current_program_enrollment(self):
        """Check if patient:
            1. Has enrolment marked current, if multiple return 1st assumed to be latest
            2. Is enrolled to any program but not marked current and if so marks latest current
            3. Is not enrolled but there is a default program and if so enrolls user to it
        :return None|PatientProgramEnrollment depending on conidtion
        """
        # 1
        enrollments = self.enrollments.filter(is_current=True)
        if enrollments.exists():
            enrollment = enrollments.first()
            return enrollment
        # 2.
        enrollments = self.enrollments.all()
        if enrollments.exists():
            enrollment = enrollments.first()
            enrollment.is_current = True
            enrollment.save()
            return enrollment
        # 3.
        programs = LoyaltyProgram.objects.filter(is_default=True)
        if programs.exists():
            enrollment = PatientProgramEnrollment.objects.create(
                patient=self,
                program=programs.first(),
                is_current=True
            )
            return enrollment
        return None

    @property
    def total_points(self):
        from orders.models import Order
        total_points = Order.objects.filter(appointment__patient=self).aggregate(
            Sum('delivery__feedback__points_awarded')
        )['delivery__feedback__points_awarded__sum']
        points = total_points if total_points else 0
        return points

    @property
    def total_redemption_points(self):
        redeemed_points = self.redemptions.all().aggregate(
            Sum("points_redeemed")
        )['points_redeemed__sum']
        points = redeemed_points if redeemed_points else 0
        return points

    @property
    def points_balance(self):
        return self.total_points - self.total_redemption_points

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}"

    def __str__(self) -> str:
        return f"Patient {self.get_full_name()}"


class PatientNextOfKeen(models.Model):
    remote_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    patient = models.ForeignKey(Patient, related_name='next_of_keen', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    class Meta:
        ordering = ['-created_at']
