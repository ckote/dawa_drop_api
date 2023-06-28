import requests
from django.conf import settings

"""from patients.mixin import FacilitySyncMixin


def get_and_sync_facilities():
    data = requests.get(f"{settings.EMR_BASE_URL}facilities/")
    if data.status_code == 200:
        mixin = FacilitySyncMixin()
        mixin.update_or_create_facilities(data.json())
"""


def get(url, params):
    return requests.get(url=url, params=params, auth=('admin', 'Admin123'))
