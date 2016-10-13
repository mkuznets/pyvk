# -*- coding: utf-8 -*-
"""
    pyvk.auth
    ~~~~~~~~~

    Implements VK authentication and cookie storage.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""

from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

from .utils import PY2

import os
import lxml.html
import requests
import hashlib
import logging
import shelve
from collections import namedtuple
from appdirs import AppDirs
from requests.exceptions import RequestException
from .exceptions import AuthError, ReqError
from .config import  RequestConfig
from .request import Request


if PY2:
    from urlparse import urlparse, ParseResult, parse_qs
    from urllib import urlencode
    from anydbm import error as db_error
else:
    from urllib.parse import urlparse, ParseResult, parse_qs, urlencode
    from dbm import error as db_error


logger = logging.getLogger(__name__)


class Auth(object):

    def __init__(self, api_id, config):
        self.config = config
        self.api_id = api_id

        self.http = requests.Session()
        self.token = None
        self.scope = None
        self.username = self.config.username
        self._state = None

        if self.config.token:
            logger.debug('Testing the token provided...')
            self.scope = self._get_token_scope(self.config.token)
            self.token = self.config.token
            logger.debug('Token is valid.')
            return

        if not self.config.username:
            logger.debug('Username is not provided. Awaiting input...')
            self.username = self.config.prompt.ask_username()

        if not self.config.disable_cache:
            try:
                cache = shelve.open(self._cache_filename, flag='r', protocol=2)
                self.http.cookies.update(cache.get('cookies', {}))
                logger.debug('Cheking cached token...')
                cached_scope = self._get_token_scope(cache['token'])
                # Token has to have at least as many permissions as requested.
                if self.config.scope <= cached_scope:
                    self.scope = cached_scope
                    self.token = cache['token']
                    logger.debug('Token is valid.')
                cache.close()
            except (KeyError, *db_error):
                logger.debug('Authorisation cache does not exist or is empty')

    @staticmethod
    def _get_token_scope(token):
        fake_auth = namedtuple('Auth', 'token')
        req = Request('account.getAppPermissions', {}, fake_auth(token=token),
                      RequestConfig(raw_response=True))
        try:
            response = req.send()
            return response['response']
        except (KeyError, ReqError) as err:
            raise AuthError('Invalid token') from err

    def auth(self):

        self._state = 'auth_page'
        args = ()

        while self._state != 'exit':

            logger.debug('Auth stage: %s' % self._state)
            fname = '_s_%s' % self._state

            assert hasattr(self, fname), 'State `%s\' not in DFA!' % self._state

            f = getattr(self, fname)

            # Cannot use pattern matching due to PY2 compatibility.
            result = f(*args)
            self._state = result[0]
            args = result[1:]

    @property
    def _cache_filename(self):
        if self.api_id is None or self.username is None:
            raise ValueError('API ID and username have to be set')

        cache_dir = AppDirs('pyvk').user_cache_dir
        if not os.path.exists(cache_dir):
            # `exist_ok' is not used for compatibility.
            os.makedirs(cache_dir)

        h = hashlib.sha1()
        h.update(str(self.api_id).encode())
        h.update(self.username.encode())
        return os.path.join(cache_dir, h.hexdigest())

    # --------------------------------------------------------------------------

    def _s_auth_page(self):

        exc_data = {'state': self._state}

        q = {'client_id': self.api_id, 'scope': self.config.scope,
             'redirect_uri': 'https://oauth.vk.com/blank.html',
             'display': 'mobile', 'v': self.config.version,
             'response_type': 'token'}

        auth_url = 'https://oauth.vk.com/authorize?%s' % urlencode(q)

        # Start auth URL
        try:
            r = self.http.get(auth_url, timeout=self.config.timeout)
        except RequestException as e:
            raise AuthError('Network error', exc=e, **exc_data)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        # Error page, try to repeat with empty cookies
        elif 'err' in url.path:
            logger.info('Cookies corrupted, trying to repeat...')
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
                raise AuthError('Unknown form action on auth page',
                                response=r, **exc_data)

    def _s_login(self, action_url, fields):

        exc_data = {'state': self._state, 'action_url': action_url,
                    'fields': fields}

        # Collect post data from the form and fill user-defined fields
        post_data = fields
        post_data['email'] = self.username
        post_data['pass'] = self.config.prompt.ask_password()

        try:
            r = self.http.post(action_url, data=post_data,
                               timeout=self.config.timeout)
        except RequestException as e:
            raise AuthError('Network error', exc=e, **exc_data)

        doc = lxml.html.document_fromstring(r.text.encode('utf-8'))

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            raise AuthError('Wrong email or password', msg=errors[0].text,
                            response=r, **exc_data)

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
            raise AuthError('Unknown form action on login page.',
                            response=r, **exc_data)

    def _s_authcheck(self, action_url, fields):

        exc_data = {'state': self._state, 'action_url': action_url,
                    'fields': fields}

        if not all(k in fields for k in ('remember', 'code')):
            raise AuthError('Authcheck page has unexpected formatting.',
                            **exc_data)

        fields['remember'] = 0
        fields['code'] = self.config.prompt.ask_secret_code()

        try:
            r = self.http.post(action_url, data=fields,
                               timeout=self.config.timeout)
        except RequestException as e:
            raise AuthError('Network error', exc=e, **exc_data)

        doc = lxml.html.document_fromstring(r.text.encode('utf-8'))

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            raise AuthError('Wrong secret code',
                            msg=errors[0].text, response=r, **exc_data)

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
            raise AuthError('Unknown form action on authcheck page.',
                            response=r, **exc_data)

    def _s_grant_access(self, action_url):

        exc_data = {'state': self._state, 'action_url': action_url}

        try:
            r = self.http.post(action_url, timeout=self.config.timeout)
        except RequestException as e:
            raise AuthError('Network error', exc=e, **exc_data)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        else:
            raise AuthError('Token fetch URL is not found', url=url, **exc_data)

    def _s_get_token(self, url):
        assert isinstance(url, ParseResult)
        self.token = parse_qs(url.fragment)['access_token'][0]

        if not self.config.disable_cache:
            try:
                cache = shelve.open(self._cache_filename, flag='n', protocol=2)
                cache['token'] = self.token
                cache['cookies'] = self.http.cookies.get_dict()
                cache.close()
            except db_error:
                logger.debug('%s: Cannot open or create cache file.'
                             % self._cache_filename)

        return ('exit', )
