import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException

from core.exceptions import BadRequestException, HTTP404NotFoundException, VerificationException

PHONE_NUMBER_TYPE = 'b2c38640-2603-4629-aebd-3b54f33f1e3a'


def find(fn, it):
    filtered = list(filter(lambda item: fn(item), it))
    return None if not filtered else filtered[0]


def get(url, params):
    return requests.get(url=url, params=params, auth=('admin', 'Admin123'))


def post(url, params, payload):
    return requests.post(url=url, params=params, json=payload, auth=("admin", 'Admin123'))


def get_identifier_types():
    uri = f"{settings.EMR_BASE_URL}patientidentifiertype"
    response = get(uri, params={})
    if response.status_code == status.HTTP_200_OK:
        return map(lambda id_: {'id': id_['uuid'], 'name': id_['display']}, response.json()['results'])
    raise APIException(
        detail=f"An error with response code {response.status_code} occurred when fetching identifier types"
    )


def search_patient(upi):
    if not upi:
        raise BadRequestException(detail='Please provide your cc number')
    params = {'client_id': upi}
    uri = f"{settings.USHAURI_BASE_URL}mohupi/search_ccc"
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['message']
        raise VerificationException()
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )


def get_user_id(usn, pwd):
    payload = {
        "user_name": usn,
        "password": pwd
    }
    uri = f"{settings.USHAURI_BASE_URL}nishauri/signin"
    response = post(uri, {}, payload)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        if data["success"]:
            return data['data']
        raise VerificationException(detail=data["msg"])
    raise BadRequestException(
        detail=f"An error with response code {response.status_code} occurred when getting remote user Id"
    )
