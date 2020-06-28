# -*- coding: utf-8 -*-
"""
    pyvk.auth
    ~~~~~~~~~

    Implements VK server- and client-side authorisation

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""

from __future__ import (generators, with_statement,
                        print_function, absolute_import)

from .utils import PY2

import os
import lxml.html
import requests
import hashlib
import logging
import traceback
import shelve
import textwrap
from appdirs import AppDirs

from .api import API
from .utils import setup_logger
from .exceptions import AuthError, ReqError, InvalidToken, APIError
from .config import ServerAuthConfig, ClientAuthConfig, GlobalConfig

if PY2:  # pragma: no cover
    from urlparse import urlparse, parse_qs, urljoin
    from anydbm import error as db_error

else:  # pragma: no cover
    from urllib.parse import urlparse, parse_qs, urljoin
    from dbm import error as db_error

logger = logging.getLogger(__name__)


class _Auth(object):
    """
    Base class for auth helper objects. Not supposed to be used directly.
    """

    token = scope = app_id = config = None

    def _test_and_set_token(self, token):
        """
        Test VK API token and store it if valid.

        :param str token: VK API token
        :raises InvalidToken: if the token proved invalid or could not be tested
        """

        api = API(token=token)
        try:
            self.scope = api.call('account.getAppPermissions')
            self.token = token

        except APIError as exc:
            raise InvalidToken(*exc.args, **exc.kwargs)

        except ReqError as exc:
            raise InvalidToken('Could not test the token', *exc.args,
                               **exc.kwargs)

    def api(self, **kwargs):
        """
        If authorised, returns an :py:class:`~pyvk.API` object.

        One can also pass keyword parameters to customise default configuration
        defined in :py:class:`~.config.GlobalConfig`
        and :py:class:`~.config.APIConfig`. The formers ones will be inherited
        if customised by the auth helper.

        :raises AuthError: if not authorised
        :returns: :py:class:`~pyvk.API` object
        """
        if self.token is None:
            raise AuthError('Not authorised. Forgot to run .auth()?')

        # Get only global parameters from the auth helper configuration...
        params = dict(GlobalConfig(**self.config))
        # ...and update them with given parameters.
        params.update(kwargs)

        return API(self.token, **params)


class ServerAuth(_Auth):

    def __init__(self, app_id, redirect_uri, **kwargs):

        self.config = ServerAuthConfig(app_id=app_id, redirect_uri=redirect_uri,
                                       **kwargs)
        setup_logger(self.config)

        self.app_id = self.config.app_id

    @property
    def auth_url(self):
        """
        Returns URL for the first step of authorisation

        :return: VK login page URL
        :rtype: str
        """
        url = 'https://oauth.vk.com/authorize' \
              '?client_id={app_id}' \
              '&display={display}' \
              '&redirect_uri={redirect_uri}' \
              '&scope={scope}' \
              '&response_type=code' \
              '&v={version}'.format(**self.config)
        return url

    def auth(self, code, client_secret):
        """
        Completes authorisation with `code` and `client_secret` provided by VK
        via GET request to `redirect_uri`.
        Initialises :py:attr:`~.ServerAuth.token`
        and :py:attr:`~.ServerAuth.scope` attributes if successful.

        :param code: parameter from GET request sent to `redirect_uri`
        :param client_secret: secret key from VK application settings
        :raises AuthError: if authorisation is unsuccessful.
        """
        url = 'https://oauth.vk.com/access_token' \
              '?client_id={app_id}' \
              '&client_secret={client_secret}' \
              '&redirect_uri={redirect_uri}' \
              '&code={code}'.format(code=code, client_secret=client_secret,
                                    **self.config)

        response = requests.get(url, timeout=self.config.timeout)

        try:
            data = response.json()
            token = data['access_token']
            self._test_and_set_token(token)

        except ValueError:
            raise AuthError('Unexpected response', response=response)

        except KeyError:
            data = response.json()
            if 'error' in data:
                raise AuthError('API Error', **data)
            else:
                raise AuthError('Unexpected JSON response', response=response)


class ClientAuth(_Auth):
    username = _state = None

    def __init__(self, **kwargs):
        self.config = ClientAuthConfig(**kwargs)
        setup_logger(self.config)

        self.http = requests.Session()

        self.app_id = (self.config.app_id
                       or self.config.input.ask('app_id'))
        self.username = (self.config.username
                         or self.config.input.ask('username'))

    def _test_and_set_cached_token(self):

        if self.config.disable_cache:
            return

        try:
            cache = shelve.open(self._cache_path, flag='r', protocol=2)
            self.http.cookies.update(cache.get('cookies', {}))

            logger.debug('Testing cached token...')
            self._test_and_set_token(cache['token'])

            # Token has to have at least as many permissions as requested.
            if self.config.scope <= self.scope:
                logger.debug('Cached token is valid.')
            else:
                logger.debug('Token does not have requested access rights')
                self.token = self.scope = None

            # NOTE: context manager is not used for Python 2 compatibility
            cache.close()

        except InvalidToken as exc:
            logger.debug('Cached token is invalid: %s' % exc.args[0])

        except db_error + (KeyError,):
            logger.debug('Authorisation cache does not exist or is empty')

    def auth(self, state=None, *args):
        """
        Starts authorisation.
        Initialises :py:attr:`~.ClientAuth.token`
        and :py:attr:`~.ClientAuth.scope` attributes if successful.

        :param str state: initial stage for authorisation procedure. Used for
                          testing purposes only.
        :raises AuthError: if authorisation is unsuccessful.
        """

        self._test_and_set_cached_token()
        if self.token:
            return

        self._state = state or 'auth_page'

        while self._state != 'exit':
            logger.debug('Auth stage: %s' % self._state)
            fname = '_s_%s' % self._state

            assert hasattr(self, fname), 'State `%s\' not in DFA!' % self._state
            f = getattr(self, fname)

            # Note: cannot use pattern matching due to Python 2 compatibility.
            result = f(*args)
            self._state = result[0]
            args = result[1:]

    @property
    def _cache_path(self):
        # Username and API ID are either passed as arguments or requested from
        # user at the point where this method is used.
        assert self.username is not None and self.app_id is not None

        cache_dir = AppDirs('pyvk').user_cache_dir
        if not os.path.exists(cache_dir):
            # `exist_ok' is not used for compatibility.
            os.makedirs(cache_dir)

        h = hashlib.sha1()
        h.update(str(self.app_id).encode())
        h.update(self.username.encode())
        return os.path.join(cache_dir, h.hexdigest())

    # --------------------------------------------------------------------------

    def _s_router(self, response):
        # Chech for JSON response in case of errors
        try:
            data = response.json()
            if 'error' in data:
                raise AuthError('Error occured', error=data)

            # No known cases of non-error JSON
            raise AuthError('Unexpected JSON response', response=response)

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
            return ('auth_page',)

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
                    return (act, act_url, dict(form.fields))

                elif act == 'grant_access':
                    return (act, act_url)

                elif act == 'authcheck_code':
                    return (act, act_url, dict(form.fields))

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

                    fields = dict((k, form.fields[k]) for k in ('code',))

                    return (act, act_url, msg, fields)

                else:
                    raise ValueError('Unrecognised action')

            except (KeyError, ValueError) as err:
                raise AuthError('Unrecognised auth page', response=response,
                                exc=err, traceback=traceback.format_exc())

    def _s_auth_page(self):
        args = dict(self.config)
        args['app_id'] = self.app_id

        url = 'https://oauth.vk.com/authorize' \
              '?client_id={app_id}' \
              '&display=mobile' \
              '&redirect_uri=https://oauth.vk.com/blank.html' \
              '&scope={scope}' \
              '&response_type=token' \
              '&v={version}'.format(**args)

        # Initiate authorisation.
        r = self.http.get(url, timeout=self.config.timeout)
        return ('router', r)

    def _s_login(self, action_url, fields):
        # Collect post data from the form and fill user-defined fields.
        fields['email'] = self.username
        fields['pass'] = self.config.input.ask('password')

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_authcheck_code(self, action_url, fields):
        fields['remember'] = 0
        fields['code'] = self.config.input.ask('secret_code')

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_security_check(self, action_url, msg, fields):
        fields['code'] = self.config.input.ask('phone', msg=msg)

        r = self.http.post(action_url, data=fields, timeout=self.config.timeout)
        return ('router', r)

    def _s_grant_access(self, action_url):
        r = self.http.post(action_url, timeout=self.config.timeout)
        return ('router', r)

    def _s_get_token(self, urlp):
        self.token, = parse_qs(urlp.fragment)['access_token']

        if not self.config.disable_cache:
            try:
                cache = shelve.open(self._cache_path, flag='n', protocol=2)
                cache['token'] = self.token
                cache['cookies'] = self.http.cookies.get_dict()
                cache.close()
            except db_error:
                logger.debug('%s: Cannot open or create cache file.'
                             % self._cache_path)
        return ('exit',)
