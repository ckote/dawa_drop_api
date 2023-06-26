import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException


PHONE_NUMBER_TYPE = 'b2c38640-2603-4629-aebd-3b54f33f1e3a'

def find(fn, it):
    filtered = list(filter(lambda item: fn(item), it))
    return None if not filtered else filtered[0]


def get(url, params):
    return requests.get(url=url, params=params, auth=('admin', 'Admin123'))


def get_identifier_types():
    uri = f"{settings.EMR_BASE_URL}patientidentifiertype"
    response = get(uri, params={})
    if response.status_code == status.HTTP_200_OK:
        return map(lambda id_: {'id': id_['uuid'], 'name': id_['display']}, response.json()['results'])
    raise APIException(
        detail=f"An error with response code {response.status_code} occurred when fetching identifier types"
    )


def search_patient(upi):
    params = {'q': upi, 'v': 'full'}
    uri = f"{settings.EMR_BASE_URL}patient"
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        return map(
            lambda patient: {
                'national_id': next((id_["identifier"] for id_ in patient['identifiers'] if
                                     id_["identifierType"]['uuid'] == 'NATIONAL_ID_TYPE'), None),
                'upi_number': next(
                    (id_["identifier"] for id_ in patient['identifiers'] if id_["identifierType"]['uuid'] == 'UPI_TYPE'),
                    None)
            },
            response.json()['results']
        )
    raise APIException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )
