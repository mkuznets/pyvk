#!/usr/bin/env python3

import os
import time
import getpass
import lxml.html
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode

import settings
from auth_cache import auth_cache
import requests


class VK(object):
    def __init__(self, api_id, permissions, username=None, password=None,
                 token=None, cache_dir=None):

        self.http = requests.Session()

        self.cache_dir = cache_dir or settings.cache_dir

        if not os.path.exists(self.cache_dir):
            # `exist_ok' is not used for compatibility.
            os.makedirs(self.cache_dir)

        elif not os.access(self.cache_dir, os.W_OK)\
                or not os.access(self.cache_dir, os.R_OK):
            raise IOError('Cannot write or read from cache directory %s' %
                          self.cache_dir)

        self.username = username or prompt.ask_user()
        self.api_id = api_id

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
            log_message('Warning: it\'s not safe to use password '
                        'authorisation')
            self.token = self._auth(start_state='login')

        elif token:
            # Token authorisation.
            if self._test_token(token):
                self.token = token
            else:
                log_message('Given token is expired or wrong, trying to get a new one...')

        if not self.token:
            # Try to get net token.
            self.token = self._auth()

        if not self.token:
            # If nothing helped
            raise AuthError('Cannot get an access token')

    def req(self, method, args={}, error_handling=True):

        args['access_token'] = self.token
        args['v'] = settings.api_version

        r = self.http.get('https://api.vk.com/method/%s?%s' % (method, urlencode(args)),
                          timeout=settings.timeout)
        result = r.json()

        # Error handling
        # TODO: MOAR ERORRS!

        if error_handling and 'error' in result:
            error_code = result['error']['error_code']
            error_msg = result['error']['error_msg']

            # User authorization failed.
            if error_code == 5:
                log_message('It seems that current token is unavailable' +
                            'now. Trying to renew...')

                # Trying to renew access token
                self.token = None
                self.token = self._auth()
                if not self.token:
                    log_message('Cannot renew access token... good bye...')

                else:
                    log_message('Access token succesfully renewed, ' +
                                'repeating the request...')
                    result = self.req(method, options)
            else:
                raise ReqError(error_msg)

        return result

    def _auth(self, start_state=None, password=None):

        # Read cache with cookies and previous token
        cache = auth_cache(self.username, self.cache_dir)

        auth = Auth(self.username, self.api_id, self.mask, cache,
                    password=password)

        return auth.token

    def _test_token(self, token):
        tmp = self.token
        self.token = token
        test = self.req('isAppUser', error_handling=False)
        self.token = tmp
        return True if 'error' not in test else False

    def _calc_mask(self, categories):
        '''
        Convert set with categories of permissions to numerical access mask.
        '''

        categories = ['notify', 'friends', 'photos', 'audio', 'video', 'offers',
                      'questions', 'pages', 'leftmenu', '', 'status', 'notes',
                      'messages', 'wall', '', 'ads', 'offline', 'docs',
                      'groups', 'notifications', 'stats', '', 'email']

        masks = {c: 2**i for i, c in enumerate(categories) if c}

        mask = 0
        for cat in categories:
            mask += masks.get(cat, 0)

        return mask


class Auth(object):

    def __init__(self, username, api_id, mask, cache, password=None, start_state=None):

        self.http = requests.Session()

        self.mask = mask
        self.api_id = api_id
        self.username = username
        self.password = password

        self.cache = cache

        self.token = None
        self.state = None

        #----------------------------------------------------------------------
        # Start state initialisation.

        cookies = cache.get_unpacked('API_COOKIES')\
            if ('API_COOKIES' in cache) else dict()
        self.http.cookies.update(cookies)

        args = ()

        if start_state:
            self.state = start_state

        else:

            if self.cache['API_TOKEN']:
                self.state = 'cached_token'

            else:
                # Start authorisation from the beginning.
                self.state = 'auth_page'

        #----------------------------------------------------------------------
        # Run DFA.

        while self.state != 'exit':

            fname = '_s_%s' % self.state
            if hasattr(self, fname):
                f = getattr(self, fname)
                self.state, *args = f(*args)

            else:
                raise RuntimeError('State `%s\' not found in auth DFA!' %
                                   self.state)

    #--------------------------------------------------------------------------
    # States.

    def _s_cached_token(self):

        # Age of the cached token
        time_diff = int(time.time()) - int(self.cache['API_TOKEN_TIME'])

        # For the cached token to be valid it has to have the same mask
        # as requested and age less than expiration time.  If these
        # conditions are satisfied, check the token by simple API req.
        if time_diff < 24 * 3600 and int(self.cache['API_MASK']) == self.mask:
            self.token = self.cache['API_TOKEN']
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
                raise RuntimeError('#Error: unpredictable behavior 1')

    def _s_login(self, action_url, fields):

        # Collect post data from the form and fill user-defined fields
        post_data = fields
        post_data['email'] = self.username
        post_data['pass'] = self.password or prompt.ask_pw()

        r = self.http.post(action_url, data=post_data, timeout=settings.timeout)

        doc = lxml.html.document_fromstring(r.text.encode())

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            print('#Error: email or password may be wrong')
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
            raise RuntimeError('#Error: login response has unexpected formatting.')

    def _s_authcheck(self, action_url, fields):

        if not ('remember' in fields and 'code' in fields):
            raise RuntimeError('#Error: authcheck page has unexpected formatting.')

        fields['remember'] = 0
        fields['code'] = prompt.ask_code()

        r = self.http.post(action_url, data=fields, timeout=settings.timeout)

        doc = lxml.html.document_fromstring(r.text.encode())

        # Check for wrong password
        errors = doc.find_class('service_msg_warning')

        if errors:
            print('#Error: secret code may be incorrect.')
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
            raise RuntimeError('#Error: response has unexpected formatting.')

    def _s_grant_access(self, action_url):

        r = self.http.post(action_url, timeout=settings.timeout)

        url = urlparse(r.url)

        # Token page
        if url.fragment.startswith('access_token='):
            return ('get_token', url)

        else:
            raise RuntimeError('#Error: unpredictable behavior 3')

    def _s_get_token(self, url):

        assert isinstance(url, ParseResult)

        # Final token
        self.token = parse_qs(url.fragment)['access_token'][0]

        # Prepare cache for cookies and token
        self.cache['API_TOKEN'] = self.token
        self.cache['API_TOKEN_TIME'] = int(time.time())
        self.cache['API_MASK'] = self.mask
        self.cache.set_packed('API_COOKIES', dict(self.http.cookies))

        # Write to cache file
        self.cache.write()

        return ('exit', )


def log_message(text, file=None):
    print('Note:', text)
    if file:
        with open(file, 'a') as log:
            log.write(text)


class prompt:
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


class AuthError(Exception):
    def __init__(self, value):
        self.value = value


class ReqError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
