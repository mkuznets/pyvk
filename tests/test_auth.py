from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import


import os
import mock
import json
import pytest
from collections import namedtuple

import pyvk
from pyvk import p_all, p_basic
from pyvk.utils import PY2, Prompt
from pyvk.auth import ClientAuth

if PY2:
    from urlparse import urlparse, parse_qsl
    from exceptions import IOError
else:
    from urllib.parse import urlparse, parse_qsl


class Session(object):
    def __init__(self, handler, **kwargs):
        self.handler = handler
        self.cookies = {}
        self.kwargs = kwargs
        super(Session, self).__init__()

    def get(self, url, *args, **kwargs):
        kwargs = dict(kwargs)
        kwargs.update(self.kwargs)
        return self.handler('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        kwargs = dict(kwargs)
        kwargs.update(self.kwargs)
        return self.handler('POST', url, *args, **kwargs)


def selector(session):
    def _callable(*args, **kwargs):
        return session
    return _callable


class Response(object):
    def __init__(self, url, content):
        self.url = url
        self.content = content

    def json(self):
        return json.loads(self.text)

    @property
    def text(self):
        return self.content.decode()


class Fake(Prompt):
    @staticmethod
    def ask(field, **kwargs):
        if field == 'secret_code':
            return 'fooooo'
        elif field == 'phone':
            return '2323442'
        elif field == 'password':
            return 'qwerty'

#  -----------------------------------------------------------------------------


def test_auth_app_invalid():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/app_invalid.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(api_id=123, username='foo', disable_cache=True)
            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_auth_unexpected_json():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/token_valid_all.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(api_id=123, username='foo', disable_cache=True)
            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_auth_user_api_id_input():

    def handler(method, url, *args, **kwargs):
        pytest.fail('No requests expected here')

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(disable_cache=True, prompt=Fake)
            assert auth.username == Fake.ask('username')
            assert auth.api_id == Fake.ask('api_id')


def test_all_stages():

    token = 'toooooo'

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/auth_page_normal.html', 'rb') as f:
                return Response(url, f.read())

        elif query.get('act', None) == 'login':
            with open('tests/static/secret_code_normal.html', 'rb') as f:
                return Response(url, f.read())

        elif query.get('act', None) == 'authcheck_code':
            with open('tests/static/security_check.html', 'rb') as f:
                return Response(url, f.read())

        elif query.get('act', None) == 'security_check':
            with open('tests/static/grant_access.html', 'rb') as f:
                return Response(url, f.read())

        elif query.get('act', None) == 'grant_access':
            with open('tests/static/grant_access.html', 'rb') as f:
                rurl = 'https://oauth.vk.com/blank.html#access_token=%s' \
                       '&expires_in=86400&user_id=101010' % token
                return Response(rurl, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):

            auth = ClientAuth(disable_cache=True, prompt=Fake,
                              username='johndoe', api_id=1234)
            auth.auth()
            assert auth.token == token


def test_incorrect_info():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/auth_page_normal.html', 'rb') as f:
                return Response(url, f.read())

        elif query.get('act', None) == 'login':
            with open('tests/static/auth_page_error.html', 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):

            auth = ClientAuth(disable_cache=True, prompt=Fake,
                              username='johndoe', api_id=1234)

            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_security_check_corrupted_page():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/security_check_corrupt.html', 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):

            auth = ClientAuth(disable_cache=True, prompt=Fake,
                              username='johndoe', api_id=1234)

            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_unrecognised_form_action():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/auth_page_unexpected_action.html', 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):

            auth = ClientAuth(disable_cache=True, prompt=Fake,
                              username='johndoe', api_id=1234)

            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_validation_failed():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/blank.html', 'rb') as f:
                rurl = 'https://oauth.vk.com/blank.html#fail=1'
                return Response(rurl, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):

            auth = ClientAuth(disable_cache=True, prompt=Fake,
                              username='johndoe', api_id=1234)

            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_corrupted_cookies():

    token = 'ttttttttttt'

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/authorize'):
            with open('tests/static/final.html', 'rb') as f:
                rurl = 'https://oauth.vk.com/blank.html#access_token=%s' \
                       '&expires_in=86400&user_id=101010' % token
                return Response(rurl, f.read())

        elif query.get('act', None) == 'grant_access':
            with open('tests/static/blank.html', 'rb') as f:
                rurl = 'https://oauth.vk.com/err=1'
                return Response(rurl, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)
    session.cookies['random'] = 42

    @mock.patch('pyvk.auth.requests.Session', new=selector(session))
    @mock.patch('pyvk.auth.requests.get', new=session.get)
    def run():
        auth = ClientAuth(disable_cache=True, prompt=Fake,
                          username='johndoe', api_id=1234)

        auth.auth('grant_access', 'https://login.vk.com/?act=grant_access')
        assert auth.token == token
        assert not session.cookies

    run()


def test_cached_token_valid():

    token = 'ttttttttttt'
    cache = {'token': token, 'cookies': {'random': 42}}

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/method'):
            assert query['access_token'] == token

            with open('tests/static/token_valid_all.json', 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    fcache = mock.MagicMock()
    fcache.__getitem__.side_effect = cache.__getitem__
    fcache.get.side_effect = cache.get
    fshelve = mock.MagicMock()
    fshelve.open.return_value = fcache

    cache_path = 'fuuuuu'

    @mock.patch('pyvk.auth.requests.Session', new=selector(session))
    @mock.patch('pyvk.auth.requests.get', new=session.get)
    @mock.patch('pyvk.auth.shelve', fshelve)
    @mock.patch('pyvk.auth.ClientAuth._cache_path', cache_path)
    def run():
        auth = ClientAuth(prompt=Fake, username='johndoe',
                          api_id=1234, scope=p_basic)
        auth.auth()
        assert auth.token == token
        assert auth.scope == p_all
        assert auth.http.cookies == cache['cookies']
        assert fshelve.open.call_args[0][0] == cache_path

    run()


def test_cached_token_invalid():

    token = 'ttttttttttt'
    cache = {'token': token, 'cookies': {'random': 42}}

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        if urlp.path.startswith('/method'):
            assert query['access_token'] == token

            with open(kwargs['file'], 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    files = [
        'tests/static/token_valid_basic.json',
        'tests/static/token_invalid.json',
        'tests/static/token_failed_test.json',
    ]

    for resp_file in files:
        session = Session(handler, file=resp_file)

        fcache = mock.MagicMock()
        fcache.__getitem__.side_effect = cache.__getitem__
        fcache.get.side_effect = cache.get
        fshelve = mock.MagicMock()
        fshelve.open.return_value = fcache

        cache_path = 'fuuuuu'

        @mock.patch('pyvk.auth.requests.Session', new=selector(session))
        @mock.patch('pyvk.auth.requests.get', new=session.get)
        @mock.patch('pyvk.auth.shelve', fshelve)
        @mock.patch('pyvk.auth.ClientAuth._cache_path', cache_path)
        def run():
            auth = ClientAuth(prompt=Fake, username='johndoe',
                              api_id=1234, scope=p_all)
            auth.auth(state='exit')
            assert auth.token is None
            assert fshelve.open.call_args[0][0] == cache_path
            assert auth.scope is None

        run()


def test_cached_filename_new_dir():

    cache = {}
    directory = 'dfdsgdsagasg'

    def handler(method, url, *args, **kwargs):
        pytest.fail('Request is either not recognised '
                    'or not expected: %s' % url)

    session = Session(handler)

    fcache = mock.MagicMock()
    fcache.__getitem__.side_effect = cache.__getitem__
    fcache.get.side_effect = cache.get
    fshelve = mock.MagicMock()
    fshelve.open.return_value = fcache

    appdirs = mock.Mock(
        return_value=namedtuple('Dir',
                                'user_cache_dir')(user_cache_dir=directory)
    )

    mk = mock.MagicMock()

    @mock.patch('pyvk.auth.requests.Session', new=selector(session))
    @mock.patch('pyvk.auth.requests.get', new=session.get)
    @mock.patch('pyvk.auth.shelve', fshelve)
    @mock.patch('pyvk.auth.AppDirs', appdirs)
    @mock.patch('pyvk.auth.os.makedirs', mk)
    def run():
        auth = ClientAuth(prompt=Fake, username='johndoe',
                          api_id=1234, scope=p_all)
        return (auth, auth._cache_path)

    # Directory exists
    with mock.patch('pyvk.auth.os.path.exists', mock.Mock(return_value=True)):
        auth, path = run()
        mk.assert_not_called()
        os.path.dirname(path) == directory
        assert os.path.basename(path)

    # Directory is created
    with mock.patch('pyvk.auth.os.path.exists', mock.Mock(return_value=False)):
        auth, path = run()
        mk.assert_called_with(directory)
        os.path.dirname(path) == directory
        assert os.path.basename(path)


def test_store_token():

    token = 'ttttttttttt'
    cookies = {'random': 42}
    cache = {}

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)

        if urlp.path.startswith('/authorize'):
            with open('tests/static/final.html', 'rb') as f:
                rurl = 'https://oauth.vk.com/blank.html#access_token=%s' \
                       '&expires_in=86400&user_id=101010' % token
                return Response(rurl, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    class Cookies(dict):
        def get_dict(self):
            return self

    session.cookies = Cookies(cookies)

    fcache = mock.MagicMock()
    fcache.__getitem__.side_effect = cache.__getitem__
    fcache.__setitem__.side_effect = cache.__setitem__
    fcache.get.side_effect = cache.get
    fshelve = mock.MagicMock()
    fshelve.open.return_value = fcache

    cache_path = 'fuuuuu'

    @mock.patch('pyvk.auth.requests.Session', new=selector(session))
    @mock.patch('pyvk.auth.requests.get', new=session.get)
    @mock.patch('pyvk.auth.shelve', fshelve)
    @mock.patch('pyvk.auth.ClientAuth._cache_path', cache_path)
    def run():
        auth = ClientAuth(prompt=Fake, username='johndoe',
                          api_id=1234, scope=p_basic)
        auth.auth()

    # Successful store
    run()
    assert cache.get('token', '') == token
    assert cache.get('cookies', '') == cookies

    # Corrupted store
    cache.clear()

    def error(self, x, a):
        # Raise one of the exceptions from db_error
        raise IOError() if PY2 else OSError

    fcache.__setitem__ = error
    run()
