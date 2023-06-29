import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse
from core.api import get
from core.exceptions import EMRException


def get_provider(uuid):
    url = f'{settings.EMR_BASE_URL}provider'
    params = {'v': 'full'}
    response = get(url=url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    raise EMRException(
        detail=f"An error with response code {response.status_code} "
               f"occurred when fetching provider from EMR",
        code=response.status_code
    )
