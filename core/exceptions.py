from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    default_detail = "Bad Request"
    default_code = status.HTTP_400_BAD_REQUEST


class HTTP404NotFoundException(APIException):
    default_detail = "Not Found"
    default_code = status.HTTP_404_NOT_FOUND


class VerificationException(APIException):
    default_detail = "CCC Number/First name combination dont match!"
    default_code = status.HTTP_403_FORBIDDEN
