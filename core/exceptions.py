from rest_framework import status
from rest_framework.exceptions import APIException


class PatientNotFoundException(APIException):
    status_code = _code = status.HTTP_404_NOT_FOUND
    default_detail = "No Such patient Found"


class OperationNotPermittedException(APIException):
    status_code = _code = status.HTTP_403_FORBIDDEN
    default_detail = "You have no permission to performer such action"


class EMRException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An error occurred fetching you data from facility"
