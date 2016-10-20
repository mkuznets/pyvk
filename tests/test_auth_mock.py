from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

import pyvk
from pyvk.utils import PY2

import mock
import json
import pytest


if PY2:
    from urlparse import urlparse, ParseResult, parse_qs
    from urllib import urlencode
else:
    from urllib.parse import urlparse, ParseResult, parse_qs, urlencode


class Session(object):
    def __init__(self, handler):
        self.handler = handler
        self.cookies = {}
        super(Session, self).__init__()

    def get(self, url, *args, **kwargs):
        return self.handler('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.handler('POST', url, *args, **kwargs)


def selector(session):
    def _callable(*args, **kwargs):
        return session
    return _callable


class Response(object):
    def __init__(self, url, text):
        self.url = url
        self.text = text

    def json(self):
        return json.loads(self.text)


@pytest.mark.skip()
def test_auth_app_invalid():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/app_invalid.json') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            with pytest.raises(pyvk.exceptions.AuthError):
                pyvk.API(api_id=123, token='foo')


@pytest.mark.skip()
def test_auth_token_only_invalid():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/token_invalid.json') as f:
            return Response(url, f.read())

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            with pytest.raises(pyvk.exceptions.AuthError):
                pyvk.API(api_id=123, token='foo')


def test_auth_token_only_valid():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        assert urlp.path.startswith('/method')
        with open('tests/static/token_valid.json') as f:
            return Response(url, f.read())

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            token = 'fuuuuuuu'
            api = pyvk.API(api_id=123, token=token)
            assert api.auth.token == token
