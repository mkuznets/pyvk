# -*- coding: utf-8 -*-
"""
    pyvk.api
    ~~~~~~~~

    Defines classes for calling VK API methods

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""

from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

import logging
import requests
import time
import json

from .config import APIConfig
from .constants import E_CAPTCHA, E_TOO_MANY, E_FLOOD
from .exceptions import ReqError, APIError
from .utils import PY2, process_args, setup_logger

if PY2:  # pragma: no cover
    from urllib import urlencode
else:    # pragma: no cover
    from urllib.parse import urlencode

logging.getLogger('requests').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class API(object):
    def __init__(self, token=None, **kwargs):
        self.config = conf = APIConfig(**kwargs)
        setup_logger(conf)
        self._token = token

        self._fixed_args = urlencode(process_args(
            {'access_token': token or None,
             'lang': conf.lang,
             'v': conf.version}
        ))

    @property
    def token(self):
        return self._token

    def __getattr__(self, prefix):
        return PartialCall([prefix], self)

    def _make_request(self, url):

        # 1. Make HTTP request
        response = requests.get(url, timeout=self.config.timeout)

        try:
            # 2. Unpack it
            data = json.loads(response.text,
                              object_hook=self.config.response_type)

        except ValueError as exc:
            raise ReqError('Response is not a valid JSON',
                           response=response, exc=exc)

        try:
            # 3. Return the result
            if self.config.raw:
                return data
            else:
                return data['response']
        except KeyError:
            # 'response' does not exist
            pass

        # 4. Handle possible API error response
        try:
            err = data['error']
            raise APIError('%s' % err['error_msg'],
                           response=response, **err)

        except KeyError as exc:
            raise ReqError('Malformed response from API',
                           response=response, data=data, exc=exc)

    def call(self, method, **args):
        conf = self.config
        args = process_args(args)
        last_exc = None

        for attempt in range(conf.max_attempts):

            url = 'https://api.vk.com/method/{method}?{fixed_args}&{args}'.format(
                method=method,
                fixed_args=self._fixed_args,
                args=urlencode(args)
            )

            try:
                return self._make_request(url)

            except APIError as exc:
                if exc.error_code in (E_TOO_MANY, E_FLOOD) and conf.auto_delay:
                    t = 0.3 * (2**attempt)
                    logger.info('Too many requests per second. '
                                'Wait %.1f sec and retry.' % t)
                    time.sleep(t)

                elif exc.error_code == E_CAPTCHA and conf.validation:
                    logger.debug('Captcha needed')
                    args['captcha_sid'] = exc.captcha_sid

                    key = conf.input.ask('captcha', img=exc.captcha_img)
                    args['captcha_key'] = key

                # Cannot handle error, raise it as is.
                else:
                    raise

            except requests.exceptions.RequestException as exc:
                last_exc = exc

        raise ReqError('Request failed after all attempts.', exc=last_exc)


class PartialCall(object):
    def __init__(self, prefix, api):
        self._prefix = prefix
        self._api = api

    @property
    def method(self):
        return '.'.join(self._prefix)

    def __getattr__(self, suffix):
        return PartialCall(self._prefix + [suffix], self._api)

    def __call__(self, **args):
        return self._api.call(self.method, **args)

    def __repr__(self):
        return '<API.%s>' % self.method
