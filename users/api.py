import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse

PHONE_NUMBER_TYPE = 'b2c38640-2603-4629-aebd-3b54f33f1e3a'

OPENMRS_ID = 'dfacd928-0370-4315-99d7-6ec1c9f7ae76'
ALIEN_ID_NUMBER = '1c7d0e5b-2068-4816-a643-8de83ab65fbf'
BIRTH_CERTIFICATE_NUMBER = '68449e5a-8829-44dd-bfef-c9c8cf2cb9b2'
CHT_RECORD_REFERENCE_UUID = 'c6552b22-f191-4557-a432-1f4df872d473'
NATIONAL_UNIQUE_PATIENT_IDENTIFIER = 'f85081e2-b4be-4e48-b3a4-7994b69bb101'
NHIF_NUMBER = '09ebf4f9-b673-4d97-b39b-04f94088ba64'
OLD_IDENTIFICATION_NUMBER = '8d79403a-c2cc-11de-8d13-0010c6dffd0f'
OPENMRS_IDENTIFICATION_NUMBER = '8d793bee-c2cc-11de-8d13-0010c6dffd0f'
PASSPORT_NUMBER = 'be9beef6-aacc-4e1f-ac4e-5babeaa1e303'
PATIENT_CLINIC_NUMBER = 'b4d66522-11fc-45c7-83e3-39a1af21ae0d'
PREP_UNIQUE_NUMBER = 'ac64e5cb-e3e2-4efa-9060-0dd715a843a1'
RECENCY_TESTING_ID = 'fd52829a-75d2-4732-8e43-4bff8e5b4f1a'
SMART_CARD_SERIAL_NUMBER = '8f842498-1c5b-11e8-accf-0ed5f89f718b'
TB_TREATMENT_NUMBER = 'c4e3caca-2dcc-4dc4-a8d9-513b6e63af91'
UNIQUE_PATIENT_NUMBER = '05ee9cf4-7242-4a17-b4d4-00f707265c8a'

WHITE_LIST_ID = [
    NHIF_NUMBER,
    PATIENT_CLINIC_NUMBER,
    UNIQUE_PATIENT_NUMBER,
    OPENMRS_ID,
    NATIONAL_UNIQUE_PATIENT_IDENTIFIER,
    PASSPORT_NUMBER,
    BIRTH_CERTIFICATE_NUMBER
]

OBSCURED_ID = [
    NHIF_NUMBER,
    PATIENT_CLINIC_NUMBER,
    NATIONAL_UNIQUE_PATIENT_IDENTIFIER,
    PASSPORT_NUMBER,
    BIRTH_CERTIFICATE_NUMBER
]


def find(fn, it):
    filtered = list(filter(lambda item: fn(item), it))
    return None if not filtered else filtered[0]


def get(url, params):
    return requests.get(url=url, params=params, auth=('admin', 'Admin123'))


def get_patient_by_uuid(uuid):
    url = f'{settings.EMR_BASE_URL}patient/{uuid}'
    response = get(url=url, params={'v': 'full'})
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    return None


def get_phone_number(attributes):
    phone_attribute = find(lambda attribute: attribute['attributeType']['uuid'] == PHONE_NUMBER_TYPE, attributes)
    if phone_attribute is not None:
        return phone_attribute['value']
    return None


def get_identifier_types():
    uri = f"{settings.EMR_BASE_URL}patientidentifiertype"
    response = get(uri, params={})
    if response.status_code == status.HTTP_200_OK:
        return map(lambda id_: {'id': id_['uuid'], 'name': id_['display']}, response.json()['results'])
    raise APIException(
        detail=f"An error with response code {response.status_code} occurred when fetching identifier types"
    )


def search_patient(upi, request):
    from .models import Patient
    from .utils import obscure_number
    params = {'q': upi, 'v': 'full'}
    uri = f"{settings.EMR_BASE_URL}patient"
    response = get(uri, params)
    if response.status_code == status.HTTP_200_OK:
        return map(
            lambda patient: {
                'uuid': patient['uuid'],
                'identifiers': map(
                    lambda identifier: {
                        # 'uuid': identifier["uuid"],
                        'id_type': identifier['identifierType']["display"],
                        'id_value': obscure_number(identifier['identifier'], "X")
                        if identifier["identifierType"]["uuid"] in OBSCURED_ID
                        else identifier['identifier']
                    },
                    filter(
                        lambda identifier: identifier["identifierType"]["uuid"] in WHITE_LIST_ID
                        , patient["identifiers"]
                    )
                ),
                'phone_number': obscure_number(get_phone_number(patient['person']['attributes'])),
                'request_verification_url': reverse(
                    viewname='users:user-request-verification',
                    request=request
                ) + f"?account={patient['uuid']}",
                'has_account': Patient.objects.filter(
                    uuid=patient['uuid']
                ).exists()
            },
            response.json()['results']
        )
        # return response.json()['results']
    raise APIException(
        detail=f"An error with response code {response.status_code} occurred when searching patient from EMR"
    )
