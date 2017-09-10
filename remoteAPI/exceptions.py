#!/usr/bin/env python3
from rest_framework import status


class ServiceError(Exception):
    """
    Base class for microservice errors

    Typically a Http response is generated from this.
    """
    def __init__(self, type, message, suggested_http_status=None):
        super().__init__(message)
        self.type = type
        self.message = message
        self.suggested_http_status = suggested_http_status


class BadRequestError(ServiceError):
    """
    Is raised when an invalid request comes from client
    """
    def __init__(self, type, message, suggested_http_status=None):
        super().__init__(type, message, suggested_http_status or status.HTTP_400_BAD_REQUEST)


class NotFoundError(ServiceError):
    """
    Is raised when a requested entity does not exist
    """
    def __init__(self, type, message):
        super().__init__(type, message, status.HTTP_404_NOT_FOUND)


class ServerError(ServiceError):
    """
    Is raised when an internal server error occurs
    """
    def __init__(self,
                 type='server_error',
                 message='Unknown error; please try again later',
                 suggested_http_status=None):
        super().__init__(type, message, suggested_http_status or status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiCallError(ServiceError):
    """
    Is raised when a valid (expected) error status is returned from a remote API call.
    """
    def __init__(self, type, message, status):
        super().__init__(type, message, status)
