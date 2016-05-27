# -----------------------------------------------------------------------------
# pyvk: vk.py
#
# Defines classes for VK API public interface, requests, and authorisation.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------


import os
import time
import getpass
import lxml.html
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode

import requests
from time import sleep
import pickle
from hashlib import md5
from appdirs import AppDirs

from . import settings


class VK(object):

    def __init__(self, api_id, permissions, username=None, password=None,
                 token=None):

        self.http = requests.Session()

        cache_dir = AppDirs('pyvk').user_cache_dir

        if not os.path.exists(cache_dir):
            # `exist_ok' is not used for compatibility.
            os.makedirs(cache_dir)

        elif not os.access(cache_dir, os.W_OK)\
                or not os.access(cache_dir, os.R_OK):
            raise IOError('Cannot write or read from cache directory %s' %
                          cache_dir)

        self.username = username or Prompt.ask_user()
        self.api_id = api_id

        self.cache_file = os.path.normpath(cache_dir) + os.sep +\
            md5(self.username.encode('utf-8')).hexdigest()

        if isinstance(permissions, int):
            # Integer value of mask.
            self.mask = permissions
        elif hasattr(permissions, '__iter__'):
            # A container with permission categories.
            self.mask = self._calc_mask(permissions)
        else:
            raise AuthError('Incorrect user permissions: %s.' % permissions)

        self.token = None

        if self.username and password:
            # Password authorisation.
            log_message('Warning: it\'s NOT SAFE to use password '
                        'authorisation')
            self.token = self._auth(start_state='auth_page')

        elif token:
            # Token authorisation.
            if self._test_token(token):
                self.token = token
            else:
                log_message('Given token is expired or wrong, trying to get '
                            'a new one...')

        if not self.token:
            # Try to get net token.
            self.token = self._auth()

        if not self.token:
            # If nothing helped
            raise AuthError('Cannot get an access token')

    def req(self, method, **args):

        args['access_token'] = self.token
        args['v'] = settings.api_version

        r = Request(method, args, self.http)

        for attempt in range(settings.MAX_ATTEMPTS):
            try:
                response = r.run()
                return response

            except ReAuthNeeded:
                # Trying to renew access token
                self.token = None
                self.token = self._auth('auth_page')
                if self.token:
                    log_message('Access token succesfully renewed, '
                                'repeating the request...')
                    r.args['access_token'] = self.token

                else:
                    log_message('Cannot renew access token... good bye...')
                    raise AuthError('Cannot renew token.')

        else:
            raise ReqError('Request failed after all attempts.')

    def _auth(self, start_state=None, password=None):

        auth = Auth(self.username, self.api_id, self.mask, self.cache_file,
                    password=password, start_state=start_state)

        return auth.token

    def _test_token(self, token):
        tmp = self.token
        self.token = token
        test = self.req('isAppUser', __eh__=False)
        self.token = tmp
        return 'error' not in test

    def _calc_mask(self, categories):
        '''
        Convert set with categories of permissions to numerical access mask.
        '''

        categories = ['notify', 'friends', 'photos', 'audio', 'video',
                      'offers', 'questions', 'pages', 'leftmenu', '', 'status',
                      'notes', 'messages', 'wall', '', 'ads', 'offline',
                      'docs', 'groups', 'notifications', 'stats', '', 'email']

        masks = {c: 2**i for i, c in enumerate(categories) if c}

        mask = 0
        for cat in categories:
            mask += masks.get(cat, 0)

        return mask


class Request(object):

    def __init__(self, method, args,  __http__):
        self.method = method
        self.args = args
        self.error_handling = args.pop('__eh__', True)
        self.http = __http__

        # Transform lists into comma-separated strings.
        self.args = {k: ','.join(str(i) for i in v) if type(v) is list else v
                     for k,v in self.args.items()}

    def run(self):

        for attempt in range(settings.MAX_ATTEMPTS):

            url = 'https://api.vk.com/method/%s?%s' \
                % (self.method, urlencode(self.args))
            r = self.http.get(url, timeout=settings.timeout)

            # TODO: is it necessary?
            result = None

            try:
                result = r.json()

            except ValueError as e:
                raise ReqError('Response is not a valid JSON') from e

            assert(isinstance(result, dict))

            # TODO: add exceptions.
            if 'response' in result:
                return result['response']

            elif 'error' in result:

                if self.error_handling:

                    err_code, err_msg = (result['error'].get(k, None) for k in
                                         ('error_code', 'error_msg'))

                    if err_code and err_msg:

                        # Handle the error and...
                        if self._handle_error(err_code, result['error'], attempt):
                            # ... retry, or...
                            continue

                        else:
                            # ... give up and raise an exception.
                            raise APIError(err_msg, err_code)

                    else:
                        raise ReqError('Error response from API is malformed')

                else:
                    return result['error']

        else:
            raise ReqError('Request failed after all attempts.')

    def _handle_error(self, error_code, error_data, attempt):

        # User authorisation failed.
        if error_code == 5 or (error_code == 10 and attempt < 2):
            log_message('It seems that current token is unavailable '
                        'now. Trying to renew...')
            raise ReAuthNeeded()

            return True

        # Too many requests.
        elif error_code in (6, 9):

            t = 0.3 * (attempt + 1)
            log_message('Too many requests per second. Wait %.1f sec and retry.' % t)
            sleep(t)

            return True

        # Captcha needed.
        elif error_code == 14:

            if 'captcha_sid' in error_data and 'captcha_img' in error_data:
                self.args['captcha_sid'] = error_data['captcha_sid']

                key = Prompt.ask_captcha(error_data['captcha_img'])
                self.args['captcha_key'] = key

                return True

            else:
                raise ReqError('Error response from API is malformed')

        # Default: don't retry the method, raise an API exception.
        return False


class Auth(object):

    def __init__(self, username, api_id, mask, cache_file, password=None,
                 start_state=None):

        self.http = requests.Session()
        self.cache_file = cache_file

        self.mask = mask
        self.api_id = api_id
        self.username = username
        self.password = password

        try:
            with open(self.cache_file, 'rb') as cf:
                self.cache = pickle.load(cf)

        except (OSError, EOFError, pickle.PickleError):
            log_message('Auth cache is corrupted or unreadable, start with '
                        'an empty cache.')
            self.cache = {}

        self.token = None
        self.state = None

        # ---------------------------------------------------------------------
        # Start state initialisation.

        cookies = self.cache.get('cookies', {})
        self.http.cookies.update(cookies)

        args = ()

        if start_state:
            self.state = start_state

        else:
            self.state = 'cached_token' \
                if ('token' in self.cache) else 'auth_page'

        # ---------------------------------------------------------------------
        # Run DFA.

        while self.state != 'exit':

            fname = '_s_%s' % self.state

            assert hasattr(self, fname), 'State `%s\' not in DFA!' % self.state

            f = getattr(self, fname)
            self.state, *args = f(*args)

    # -------------------------------------------------------------------------
    # States.

    def _s_cached_token(self):

        assert(all(k in self.cache for k in ('token_time', 'mask', 'token')))

        # Age of the cached token
        time_diff = int(time.time()) - int(self.cache['token_time'])

        # For the cached token to be valid it has to have the same mask
        # as requested and age less than expiration time.  If these
        # conditions are satisfied, check the token by simple API req.
        if time_diff < 24 * 3600 and int(self.cache['mask']) == self.mask:
            self.token = self.cache['token']
            return ('exit', )

        else:
            return ('auth_page', )

    def _s_auth_page(self):

        q = {'client_id': self.api_id, 'scope': self.mask,
             'redirect_uri': 'https://oauth.vk.com/blank.html',
             'display': 'mobile', 'v': settings.api_version,
             'response_type': 'token'}

        auth_url = 'https://oauth.vk.com/authorize?%s' % urlencode(q)

        # Start auth URL
        r = self.http.get(auth_url, timeout=settings.timeout)
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
            doc = lxml.html.document_fromstring(r.text.encode())
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
        post_data['pass'] = self.password or Prompt.ask_pw()

        r = self.http.post(action_url, data=post_data, timeout=settings.timeout)

        doc = lxml.html.document_fromstring(r.text.encode())

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            log_message('Email or password may be wrong')
            # TODO: print error text from page
            return ('login', action_url, fields)

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
        fields['code'] = Prompt.ask_code()

        r = self.http.post(action_url, data=fields, timeout=settings.timeout)

        doc = lxml.html.document_fromstring(r.text.encode())

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            log_message('Secret code may be incorrect.')
            # TODO: print error text from page
            return ('authcheck', action_url, fields)

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

        r = self.http.post(action_url, timeout=settings.timeout)

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

        # Prepare cache for cookies and token
        self.cache = {'token': self.token, 'token_time': int(time.time()),
                      'mask': self.mask, 'cookies': dict(self.http.cookies)}

        # Write to cache file
        with open(self.cache_file, 'wb') as cf:
            pickle.dump(self.cache, cf)

        return ('exit', )


def log_message(text, file=None):
    print('Note:', text)
    if file:
        with open(file, 'a') as log:
            log.write(text)


class Prompt:

    def ask_pw():
        print()
        return getpass.getpass()

    def ask_user():
        username = input('Username (email of mobile number): ')
        return username.strip()

    def ask_code():

        while True:
            code = input('Secret code: ').strip()
            if not (code.isdigit() and len(code) == 6):
                print('The code must be a 6-digit number.')
                continue
            break

        return int(code)

    def ask_captcha(url):

        print(url)
        key = input('Enter symbols from the picture: ').strip()

        return key


# -----------------------------------------------------------------------------

class VKError(Exception):
    pass


class AuthError(VKError):
    def __init__(self, value):
        self.value = value


class ReAuthNeeded(VKError):
    def __init__(self):
        pass


class ReqError(VKError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APIError(VKError):

    def __init__(self, msg, code):
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'Error #%d: %s' % (self.code, self.msg)
