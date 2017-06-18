#!/usr/bin/env python3
import logging

import jwt
import requests
from appdarchi.exceptions import ApiCallError, ServerError
from django.http.response import JsonResponse
from django.utils.translation import ugettext_lazy as _
from settings import JWT_SECRET_KEY, ServiceDNS, Services, TOKEN_EMAIL

logger = logging.getLogger(__name__)


def generate_privileged_token():
    return jwt.encode({'email': TOKEN_EMAIL}, JWT_SECRET_KEY)


def send_request(
        method,
        service,
        url,
        data=None,
        params=None,
        files=None,
        token=None,
        raise_exception=True):
    if service == Services.CAPI:
        token = generate_privileged_token()

    url = ServiceDNS[service] + url
    return _send_request(method, url, data, params, files, {'Authorization': token}, raise_exception)


def _send_request(
        method,
        url,
        data,
        params,
        files,
        headers,
        raise_exception=True):
    if isinstance(method, str):
        method = getattr(requests, method)

    response = method(url, headers=headers, data=data, files=files, params=params, timeout=10)

    if response.headers.get('content-type') != 'application/json':
        if raise_exception:
            raise ServerError()
        else:
            return JsonResponse({
                'type': 'error',
                'message': 'invalid content type',
            })

    if response.status_code >= 300:
        data = response.json()
        if 'type' not in data or 'message' not in data:
            logger.error('Wrong response data format')

        if raise_exception:
            raise ApiCallError(
                data.get('type', 'error'),
                data.get('message', _('Error')),
                response.status_code
            )

    return response
