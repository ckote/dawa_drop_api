from django.conf import settings

from patients.models import Patient
from patients.serializers import PatientAddUpdateSerializer
from users.serializers import UserSerializer, ProfileSerializer
import requests


def obscure_email(email):
    username, domain = email.split("@")
    obscured_email = '{}{}@{}'.format(username[:2], '*' * len(username[2:]), domain)
    return obscured_email


def obscure_number(number, char="*", start=3, end=-2):
    if number:
        return '{}{}{}'.format(number[:start], char * len(number[start:end]), number[end:])
    return None


def update_patient(patient, request):
    # update user
    user = request.user
    user_serializer = UserSerializer(instance=user, data=patient)
    profile_serializer = ProfileSerializer(instance=user.profile, data=patient)
    user_serializer.is_valid(raise_exception=True)
    profile_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    profile = profile_serializer.save()
    p = Patient.objects.get_or_create(user=user)[0]
    patient_serializer = PatientAddUpdateSerializer(instance=p, data=patient)
    patient_serializer.is_valid(raise_exception=True)
    patient = patient_serializer.save()


def post_appointment_to_emr(data: dict):
    return requests.post(f"{settings.EMR_BASE_URL}medication/appointments/", data=data)
