# -----------------------------------------------------------------------------
# pyvk: auth.py
#
#
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------

from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

from .utils import PY2

import os
import time
import lxml.html
import requests
import pickle
import binascii
from appdirs import AppDirs

from . import settings
from .exceptions import AuthError, PyVKError
from .request import Request
from .utils import Prompt, log_message


if PY2:
    from urlparse import urlparse, ParseResult, parse_qs
    from urllib import urlencode
else:
    from urllib.parse import urlparse, ParseResult, parse_qs, urlencode


p_notify = 1
p_friends = 2
p_photos = 4
p_audio = 8
p_video = 16
p_offers = 32
p_questions = 64
p_pages = 128
p_leftmenu = 256
p_status = 1024
p_notes = 2048
p_messages = 4096
p_wall = 8192
p_ads = 32768
p_offline = 65536
p_docs = 131072
p_groups = 262144
p_notifications = 524288
p_stats = 1048576
p_email = 4194304
p_market = 134217728


p_all = p_notify | p_friends | p_photos | p_audio | p_video \
    | p_offers | p_questions | p_pages | p_leftmenu | p_status \
    | p_notes | p_messages | p_wall | p_ads | p_offline | p_docs \
    | p_groups | p_notifications | p_stats | p_email | p_market


p_basic = p_friends | p_photos | p_audio | p_video | p_status | p_messages \
    | p_wall | p_groups


class Auth(object):

    def __init__(self, api_id, **kwargs):

        self.http = requests.Session()

        self.api_id = api_id
        self.scope = kwargs.get('scope', p_basic)

        self.username = None
        self.token = None

        # ---------------------------------------------------------------------

        if 'token' in kwargs:
            try:
                self.test_token(kwargs['token'])

            except PyVKError as e:
                raise AuthError('Invalid token', **e.attrs)

            else:
                self.token = kwargs['token']
                return

        # ---------------------------------------------------------------------

        for name, default in settings.options('auth'):
            setattr(self, name, kwargs.get(name, default))

        self.prompt = kwargs.get('prompt', Prompt)

        self.username = kwargs.get('username', None)
        if not self.username:
            self.username = self.prompt.ask_username()

        if not self.disable_cache:

            self.cache = Cache(self.username)
            cached = self.cache.read()

            if cached:
                cookies = cached.get('cookies', {})
                self.http.cookies.update(cookies)

                # set() added for PY2 compatibility.
                assert {'token_time', 'scope', 'token'} <= set(cached.keys())

                # Age of the cached token
                time_diff = int(time.time()) - cached['token_time']

                # For the cached token to be valid it has to have the same mask
                # as requested and age less than expiration time.
                if time_diff < 24 * 3600 and cached['scope'] <= self.scope:
                    try:
                        real_scope = self.test_token(cached['token'])
                    except PyVKError as e:
                        pass
                    else:
                        self.token = cached['token']
                        self.scope = real_scope


    def test_token(self, token):
        req = Request('account.getAppPermissions', token=token)
        data = req.run()
        return data

    def auth(self):

        if not self.username:
            raise AuthError('Cannot authorise: username is not given')

        self.state = 'auth_page'
        args = ()

        while self.state != 'exit':

            fname = '_s_%s' % self.state

            assert hasattr(self, fname), 'State `%s\' not in DFA!' % self.state

            f = getattr(self, fname)

            # Cannot use pattern matching due to PY2 compatibility.
            result = f(*args)
            self.state = result[0]
            args = result[1:]

    def _s_auth_page(self):

        q = {'client_id': self.api_id, 'scope': self.scope,
             'redirect_uri': 'https://oauth.vk.com/blank.html',
             'display': 'mobile', 'v': self.version,
             'response_type': 'token'}

        auth_url = 'https://oauth.vk.com/authorize?%s' % urlencode(q)

        # Start auth URL
        r = self.http.get(auth_url, timeout=self.timeout)
        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        # Error page, try to repeat with empty cookies
        elif 'err' in url.path:
            log_message('cookies corrupted, trying to repeat...')

            self.http.cookies.clear()
            return ('auth_page', )

        else:
            # TODO: fix the ugly parsing
            doc = lxml.html.document_fromstring(r.text.encode('utf-8'))
            form = doc.forms[0]
            action_url = urlparse(form.action)
            act = parse_qs(action_url.query)['act'][0]

            if act == 'login':
                return ('login', form.action, dict(form.fields))

            elif act == 'grant_access':
                return ('grant_access', form.action)

            else:
                raise AuthError('Unpredictable behavior 1')

    def _s_login(self, action_url, fields):

        # Collect post data from the form and fill user-defined fields
        post_data = fields
        post_data['email'] = self.username
        post_data['pass'] = self.prompt.ask_password()

        r = self.http.post(action_url, data=post_data,
                           timeout=self.timeout)

        doc = lxml.html.document_fromstring(r.text.encode('utf-8'))

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            raise AuthError('Wrong email or password',
                            msg=errors[0].text, response=r)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        # Otherwise: check the need to confirm access
        form = doc.forms[0]
        action_url = urlparse(form.action)
        act = parse_qs(action_url.query)['act'][0]

        if act == 'grant_access':
            return ('grant_access', form.action)

        elif act == 'authcheck_code':
            action_url = '%s://%s%s' % (url.scheme, url.netloc, form.action)
            return ('authcheck', action_url, dict(form.fields))

        else:
            raise AuthError('Login response has unexpected formatting.')

    def _s_authcheck(self, action_url, fields):

        if not all(k in fields for k in ('remember', 'code')):
            raise AuthError('Authcheck page has unexpected formatting.')

        fields['remember'] = 0
        fields['code'] = self.prompt.ask_secret_code()

        r = self.http.post(action_url, data=fields, timeout=self.timeout)

        doc = lxml.html.document_fromstring(r.text.encode('utf-8'))

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            raise AuthError('Wrong secret code',
                            msg=errors[0].text, response=r)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        # Otherwise: check the need to confirm access
        form = doc.forms[0]
        action_url = urlparse(form.action)
        act = parse_qs(action_url.query)['act'][0]

        if act == 'grant_access':
            return ('grant_access', form.action)

        else:
            raise AuthError('Response has unexpected formatting.')

    def _s_grant_access(self, action_url):

        r = self.http.post(action_url, timeout=self.timeout)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        else:
            raise AuthError('Unpredictable behavior 3')

    def _s_get_token(self, url):

        assert isinstance(url, ParseResult)

        # Final token
        self.token = parse_qs(url.fragment)['access_token'][0]

        if not self.disable_cache:
            self.cache.write(token=self.token, scope=self.scope,
                             token_time=int(time.time()),
                             cookies=self.http.cookies.get_dict())

        return ('exit', )


class Cache(object):

    def __init__(self, username):

        cache_dir = AppDirs('pyvk').user_cache_dir

        if not os.path.exists(cache_dir):
            # `exist_ok' is not used for compatibility.
            os.makedirs(cache_dir)

        cache_hash = binascii.crc32(username.encode('utf-8'))
        self.file = os.path.join(cache_dir, str(cache_hash))

    def read(self):
        try:
            with open(self.file, 'rb') as cf:
                return pickle.load(cf)

        except (OSError, IOError, EOFError, pickle.PickleError):
            # Auth cache is corrupted or unreadable, start with an empty cache
            return {}

    def write(self, **data):
        with open(self.file, 'wb') as cf:
            pickle.dump(data, cf, protocol=2)
