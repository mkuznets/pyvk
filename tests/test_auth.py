from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import


import mock
import pytest
from collections import namedtuple

import pyvk
from pyvk import p_all, p_basic
from pyvk.utils import PY2
from pyvk import ClientAuth, ServerAuth

from tests.utils import *

if PY2:
    from urlparse import urlparse, parse_qsl
    from exceptions import IOError
else:
    from urllib.parse import urlparse, parse_qsl


def test_auth_app_invalid():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/app_invalid.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(app_id=123, username='foo', disable_cache=True)
            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_auth_unexpected_json():

    def handler(method, url, *args, **kwargs):
        with open('tests/static/token_valid_all.json', 'rb') as f:
            return Response(url, f.read())

    session = Session(handler)
    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(app_id=123, username='foo', disable_cache=True)
            with pytest.raises(pyvk.exceptions.AuthError):
                auth.auth()


def test_auth_user_app_id_input():

    def handler(method, url, *args, **kwargs):
        pytest.fail('No requests expected here')

    session = Session(handler)

    with mock.patch('pyvk.auth.requests.Session', new=selector(session)):
        with mock.patch('pyvk.auth.requests.get', new=session.get):
            auth = ClientAuth(disable_cache=True, input=Fake)
            assert auth.username == Fake.ask('username')
            assert auth.app_id == Fake.ask('app_id')


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

            version = '5.0'

            auth = ClientAuth(disable_cache=True, input=Fake,
                              username='johndoe', app_id=1234, version=version)
            auth.auth()
            assert auth.token == token

            # Test .get_api()
            api = auth.api(lang='ru')
            # Config propagation
            assert api.config.version == version
            assert api.config.lang == 'ru'
            assert api.token == token


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

            auth = ClientAuth(disable_cache=True, input=Fake,
                              username='johndoe', app_id=1234)

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

            auth = ClientAuth(disable_cache=True, input=Fake,
                              username='johndoe', app_id=1234)

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

            auth = ClientAuth(disable_cache=True, input=Fake,
                              username='johndoe', app_id=1234)

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

            auth = ClientAuth(disable_cache=True, input=Fake,
                              username='johndoe', app_id=1234)

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
        auth = ClientAuth(disable_cache=True, input=Fake,
                          username='johndoe', app_id=1234)

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
        auth = ClientAuth(input=Fake, username='johndoe',
                          app_id=1234, scope=p_basic)
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
            auth = ClientAuth(input=Fake, username='johndoe',
                              app_id=1234, scope=p_all)
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
        auth = ClientAuth(input=Fake, username='johndoe',
                          app_id=1234, scope=p_all)
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
        auth = ClientAuth(input=Fake, username='johndoe',
                          app_id=1234, scope=p_basic)
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


def test_server_auth():

    def handler(method, url, *args, **kwargs):
        urlp = urlparse(url)
        query = dict(parse_qsl(urlp.query))

        responses = {
            'valid': 'tests/static/server_auth_token.json',
            'non_json': 'tests/static/server_auth_non_json.html',
            'error': 'tests/static/server_auth_error.json',
            'unrecognised': 'tests/static/server_auth_unrecognised.json',
        }

        if urlp.path.startswith('/method'):
            assert query['access_token'] == 'fooo'
            with open('tests/static/token_valid.json', 'rb') as f:
                return Response(url, f.read())

        elif urlp.path.startswith('/access_token'):
            with open(responses[query['code']], 'rb') as f:
                return Response(url, f.read())

        else:
            pytest.fail('Request is either not recognised '
                        'or not expected: %s' % url)

    session = Session(handler)

    @mock.patch('pyvk.auth.requests.Session', new=selector(session))
    @mock.patch('pyvk.auth.requests.get', new=session.get)
    def run():
        url = 'appserver.com'
        auth = ServerAuth(1234, url)
        assert url in auth.auth_url

        auth.auth('valid', '123')
        assert auth.token == 'fooo'

        with pytest.raises(pyvk.exceptions.AuthError):
            auth.auth('error', '123')

        with pytest.raises(pyvk.exceptions.AuthError):
            auth.auth('non_json', '123')

        with pytest.raises(pyvk.exceptions.AuthError):
            auth.auth('unrecognised', '123')

    run()


def test_get_api():
    auth = ServerAuth(1234, 'aaa')
    with pytest.raises(pyvk.exceptions.AuthError):
        auth.api()
