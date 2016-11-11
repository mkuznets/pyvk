from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import


import os
import mock
import pytest
from collections import namedtuple

import pyvk
from pyvk import p_all, p_basic
from pyvk.utils import PY2
from pyvk import API

from tests.utils import *

if PY2:
    from urlparse import urlparse, parse_qsl
else:
    from urllib.parse import urlparse, parse_qsl


def test_invalid_json():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/api_corrupt.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.get', new=session.get):
        api = API()
        with pytest.raises(pyvk.exceptions.ReqError):
            api.vk.test()


def test_valid_json():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/api_valid.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.get', new=session.get):
        api = API(raw_response=True)
        data = api.vk.test()
        assert 'response' in data


def test_too_many():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/api_too_many.json', 'rb') as f:
            return Response(url, f.read())

    sleep = mock.Mock()

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.get', new=session.get):
        with mock.patch('time.sleep', new=sleep):

            api = API(max_attempts=2)

            with pytest.raises(pyvk.exceptions.ReqError):
                api.vk.test()

    sleep.assert_called()


def test_captcha():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if 'captcha_sid' in query:
            assert query['captcha_key'] == 'fooooo'
            with open('tests/static/api_valid.json', 'rb') as f:
                return Response(url, f.read())

        else:
            with open('tests/static/api_captcha.json', 'rb') as f:
                return Response(url, f.read())

    class FakeCaptcha(Input):
        @staticmethod
        def ask(field, **kwargs):
            if field == 'captcha':
                assert 'img' in kwargs
                return 'fooooo'

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.get', new=session.get):

        api = API(max_attempts=2, input=FakeCaptcha)
        api.vk.test()
