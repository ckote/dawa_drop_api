import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse
from core.api import get
from core.exceptions import EMRException


def get_patient_encounters(uuid):
    url = f'{settings.EMR_BASE_URL}encounter'
    params = {'v': 'full', 'patient': uuid}
    response = get(url=url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()['results']
    raise EMRException(
        detail=f"An error with response code {response.status_code} "
               f"occurred when fetching visit information from EMR",
        code=response.status_code
    )


def get_encounter_type(uuid):
    url = f'{settings.EMR_BASE_URL}encountertype/{uuid}'
    params = {'v': 'full'}
    response = get(url=url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    raise EMRException(
        detail=f"An error with response code {response.status_code} "
               f"occurred when fetching visit type from EMR",
        code=response.status_code
    )


def get_encounter_types():
    url = f'{settings.EMR_BASE_URL}encountertype'
    params = {'v': 'full'}
    response = get(url=url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()['results']
    raise EMRException(
        detail=f"An error with response code {response.status_code} "
               f"occurred when fetching visit types from EMR",
        code=response.status_code
    )

