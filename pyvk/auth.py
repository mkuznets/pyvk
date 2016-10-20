# -*- coding: utf-8 -*-
"""
    pyvk.auth
    ~~~~~~~~~

    Implements VK authentication and cookie storage.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""

from __future__ import generators, with_statement, print_function, absolute_import

from .utils import PY2

import os
import lxml.html
import requests
import hashlib
import logging
import shelve
import textwrap
from appdirs import AppDirs
from .exceptions import AuthError, ReqError, InvalidToken, APIError
from .config import RequestConfig
from .request import Request
from requests.exceptions import RequestException


if PY2:
    from urlparse import urlparse, parse_qs, urljoin
    from urllib import urlencode
    from anydbm import error as db_error
else:
    from urllib.parse import urlparse, parse_qs, urlencode, urljoin
    from dbm import error as db_error


logger = logging.getLogger(__name__)


class Auth(object):

    def __init__(self, config):
        self.config = config

        self.http = requests.Session()
        self.token = None
        self.scope = None
        self.api_id = self.config.api_id
        self.username = self.config.username
        self._state = None

        if self.config.token:
            logger.debug('Testing the token provided...')
            self._test_and_set_token(self.config.token)
            logger.debug('Token is valid.')
            return

        if not self.config.username:
            logger.info('Username is not provided')
            self.username = self.config.prompt.ask_username()

        if not self.config.disable_cache:
            try:
                cache = shelve.open(self._cache_filename, flag='r', protocol=2)
                self.http.cookies.update(cache.get('cookies', {}))

                logger.debug('Cheking cached token...')
                self._test_and_set_token(cache['token'])

                # Token has to have at least as many permissions as requested.
                if self.config.scope <= self.scope:
                    logger.debug('Token is valid.')
                else:
                    # TODO: Cached token does not have enough permission
                    self.token = None
                    self.scope = None
                cache.close()

            except RequestException:
                raise

            except InvalidToken as err:
                logger.debug('Cached token is invalid: %s' % err.args[0])

            except db_error + (KeyError, ):
                logger.debug('Authorisation cache does not exist or is empty')

    def _test_and_set_token(self, token):
        self.token = token
        req = Request('account.getAppPermissions', {}, self,
                      RequestConfig(auto_reauth=False))
        try:
            self.scope = req.send()

        except APIError as err:
            self.token = None
            raise InvalidToken(err.msg, exc=err)

        except ReqError as err:
            self.token = None
            raise InvalidToken('Could not test the token', exc=err)

    def auth(self, state=None, *args):
        self._state = state or 'auth_page'

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

    def _s_router(self, response):
        # Chech for JSON response in case of errors
        try:
            data = response.json()
            if 'error' in data:
                raise AuthError('Error occured', error=data)
        except ValueError:
            # Not JSON, treat response as HTML
            pass

        urlp = urlparse(response.url)

        # Detect token page
        if urlp.fragment.startswith('access_token='):
            return ('get_token', urlp)

        # Detect failed validation
        elif 'fail=1' in urlp.fragment:
            raise AuthError('Unsuccesful validation', response=response)

        # Detect error page, try to repeat with empty cookies
        elif 'err' in urlp.path:
            logger.debug('Error occured, trying to repeat...')
            self.http.cookies.clear()
            return ('auth_page', )

        # Parse HTML
        else:
            try:
                doc = lxml.html.fromstring(response.content)

                errors = doc.find_class('service_msg_warning')
                if errors:
                    raise AuthError('Incorrect information',
                                    msg=errors[0].text, response=response)

                form, = doc.forms
                # Make sure action_url is full i.e. contains scheme and host
                act_url = urljoin(response.url, form.action)
                act, = parse_qs(urlparse(act_url).query)['act']

                if act == 'login':
                    fields = {k: form.fields[k] for k in ('email', 'pass')}
                    return (act, act_url, dict(form.fields))

                elif act == 'grant_access':
                    return (act, act_url)

                elif act == 'authcheck_code':
                    fields = {k: form.fields[k] for k in ('remember', 'code')}
                    return (act, act_url, fields)

                elif act == 'security_check':
                    prefixes = doc.xpath("//span[@class='field_prefix']")
                    if len(prefixes) != 2:
                        raise ValueError('Unrecognised security page')

                    # Phone number: construct from prefix and suffix
                    prefixes_text = [p.text_content().strip() for p in prefixes]
                    prefixes_text.insert(1, ' ... ')
                    number = ''.join(prefixes_text)

                    # Text message
                    msgs = doc.xpath("//div[@class='fi_row']")[:2]
                    msg = "\n".join([m.text_content() for m in msgs])
                    # Wrap for width 70
                    msg = "\n".join(textwrap.wrap(msg))
                    msg += "\n%s: " % number

                    fields = {k: form.fields[k] for k in ('code',)}

                    return (act, act_url, msg, fields)

                else:
                    raise ValueError('Unrecognised action')

            except (KeyError, ValueError) as err:
                raise AuthError('Unrecognised auth page', response=response,
                                exc=err)

    def _s_auth_page(self):
        q = {'client_id': self.api_id, 'scope': self.config.scope,
             'redirect_uri': 'https://oauth.vk.com/blank.html',
             'display': 'mobile', 'v': self.config.version,
             'response_type': 'token'}

        # Initiate authorisation.
        r = self.http.get('https://oauth.vk.com/authorize?%s' % urlencode(q),
                          timeout=self.config.timeout)
        return ('router', r)

    def _s_login(self, action_url, fields):
        # Collect post data from the form and fill user-defined fields.
        fields['email'] = self.username
        fields['pass'] = self.config.prompt.ask_password()

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_authcheck_code(self, action_url, fields):
        fields['remember'] = 0
        fields['code'] = self.config.prompt.ask_secret_code()

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_security_check(self, action_url, msg, fields):
        fields['code'] = self.config.prompt.ask_text(msg)

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_grant_access(self, action_url):
        r = self.http.post(action_url, timeout=self.config.timeout)
        return ('router', r)

    def _s_get_token(self, urlp):
        self.token, = parse_qs(urlp.fragment)['access_token']

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
