# -----------------------------------------------------------------------------
# pyvk: request.py
#
#
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------

from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

import requests
from requests.exceptions import RequestException

from . import settings
from .utils import PY2
from .exceptions import ReqError, APIError

if PY2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode


class Request(object):

    def __init__(self, method, args=None, **kwargs):
        self.method = method
        self.args = args or {}

        for name, default in settings.options('req'):
            setattr(self, name, kwargs.get(name, default))

        if 'token' in kwargs:
            self.args['access_token'] = kwargs['token']

        # Transform lists into comma-separated strings.
        self.args = {k: ','.join(str(i) for i in v) if type(v) is list else v
                     for k, v in self.args.items()}

    def run(self):

        url = 'https://api.vk.com/method/%s?%s' \
            % (self.method, urlencode(self.args))

        try:
            response = requests.get(url, timeout=self.timeout)

        except RequestException as e:
            raise ReqError('Network error', exc=e)

        # -----------------------------------------------------------------

        try:
            data = response.json()

        except ValueError as e:
            raise ReqError('Response is not a valid JSON',
                           response=response, exc=e)

        # -----------------------------------------------------------------

        assert isinstance(data, dict)

        try:
            return data['response']

        except KeyError:
            if not self.error_handling:
                return data

        # -----------------------------------------------------------------

        try:
            err = data['error']
            err_code, err_msg = err['error_code'], err['error_msg']

        except KeyError as e:
            raise ReqError('Error response from API is malformed',
                           response=response, data=data, exc=e)

        # -----------------------------------------------------------------

        raise APIError('VK API returned an error', code=err_code,
                       msg=err_msg, error=err, response=response)
