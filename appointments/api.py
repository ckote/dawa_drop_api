import requests

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from core.exceptions import BadRequestException, HTTP404NotFoundException, VerificationException
from users.api import get, post


def get_appointments(user_id, future=False):
    uri = f"{settings.USHAURI_BASE_URL}nishauri/{'appointment_previous' if future else 'appointment_previous'}"
    params = {'user_id': user_id}
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['data']
        raise VerificationException(detail=data['data'])
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )


def get_current_appointments(user_id):
    uri = f"{settings.USHAURI_BASE_URL}nishauri/current_appt"
    params = {'user_id': user_id}
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['data']
        raise VerificationException(detail=data['data'])
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )


def get_missed_appointments(user_id):
    uri = f"{settings.USHAURI_BASE_URL}nishauri/appointment_missed"
    params = {'user_id': user_id}
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['data']
        raise VerificationException(detail=data['data'])
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )


def get_appointment_trends(user_id):
    uri = f"{settings.USHAURI_BASE_URL}nishauri/appointment_trends"
    params = {'user_id': user_id}
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['data']
        raise VerificationException(detail=data['data'])
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )
