#!/usr/bin/env python3

import os
import sys
import time
import configparser
import getpass
import lxml.html
from urllib.parse import urlparse, ParseResult, parse_qs

import settings
from browser import browser
from auth_cache import auth_cache


def log_message(text, file=None):
    print('Note: ' + text, file=sys.stderr)
    if file:
        with open(file, 'a') as log:
            log.write(text)


class user_interaction:
    def ask_pw():
        return getpass.getpass()


class AuthError(Exception):
    def __init__(self, value):
        self.value = value


class ReqError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Error(Exception):
    def __init__(self, value):
        self.value = value


class vk:
    def __init__(self, token=None, email=None, number=None, password=None,
                 api_id=None, mask=None, access=None,
                 cache_dir=settings.cache_dir):
        try:
            if (not mask and not access):
                raise AuthError('Access mask or categories are required')
            if (not api_id):
                raise AuthError('API_ID is required')
            if (not cache_dir):
                raise AuthError('Directory for cache is required')

            self.http = browser()

            if os.access(cache_dir, os.W_OK) and os.access(cache_dir, os.R_OK):
                self.cache_dir = cache_dir
            else:
                raise AuthError('Given cache directory is not writable' +
                                'and readable')

            self.mask = self.access_mask(access) if access else mask
            self.api_id = api_id

            self.username = email if email else number
            self.token = None

            # Use only password
            if (self.username and password):
                log_message('Remember: it\' not safe to use password' +
                            'for authorization')
                self.token = self.auth(start_state='login')

            # A given token (can be used without username)
            elif (token):
                if self.check_token(token):
                    self.token = token
                else:
                    if (self.username):
                        log_message('Given token is expired or wrong,' +
                                    'trying to get a new one...')
                        self.token = self.auth()
                    else:
                        raise AuthError('You must provide email for' +
                                        'authorization')

            # Username without any token
            elif(self.username):
                log_message('Looking for a cached token...')
                self.token = self.auth()

            else:
                raise AuthError('It seems you did not provide enough' +
                                'information for authorization')

            # If nothing helped
            if not self.token:
                raise AuthError('Cannot get an access token')

        except AuthError as msg:
            print("Init error: " + msg.value)
            sys.exit(2)

    def req(self, method, options={}, error_handling=True):
        try:
            options['access_token'] = self.token

            self.http.set_url('https://api.vk.com/method/' + method)
            self.http.set_get_param(options)

            self.http.req_get()
            result = self.http.json()

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
                    self.token = self.auth()
                    if not self.token:
                        log_message('Cannot renew access token... good bye...')
                        quit()
                    else:
                        log_message('Access token succesfully renewed,' +
                                    'repeating the request...')
                        result = self.req(method, options)
                else:
                    raise ReqError(error_msg)

        except ReqError as e:
            raise

        #######################

        return result

    def auth(self, start_state=None):

        # Read cache with cookies and previous token
        cache = auth_cache(self.username, self.cache_dir)

        token = ''

        # Set of avaliable states of the autorization DFA
        states = {'check_token', 'auth_page', 'login', 'grant_access',
                  'get_token' 'exit'}

        # Default state (unless a cached token is valid)
        state = 'auth_page'

        # If token is cached, start from checking it for validity.
        if cache['API_TOKEN'] != '':
            log_message('Cache token found')

            # Age of the cached token
            time_diff = int(time.time()) - int(cache['API_TOKEN_TIME'])

            # For the cached token to be valid it has to have the same mask
            # as requested and age less than expiration time.  If these
            # conditions are satisfied, check the token by simple API req.
            if time_diff < settings.expire_time\
                    and cache['API_MASK'] == str(self.mask)\
                    and self.check_token(cache['API_TOKEN']):
                return cache['API_TOKEN']
            else:
                log_message('Cached token failed.')

        cookies = cache.get_unpacked('API_COOKIES')\
            if ('API_COOKIES' in cache) else dict()
        self.http.set_cookies(cookies)

        # Authorization DFA
        while state != 'exit':

            log_message('Auth DFA state: ' + state)

            # Standard auth
            if state == 'auth_page':

                auth_url = 'https://' + \
                    'api.vk.com' + \
                    '/oauth/authorize?' + \
                    'client_id=' + str(self.api_id) + '&' + \
                    'scope=' + str(self.mask) + '&' + \
                    'redirect_uri=http://api.vk.com/blank.html&' + \
                    'display=mobile&' + \
                    'response_type=token'

                # Start auth URL
                self.http.set_url(auth_url)
                self.http.req_get()

                url = self.http.url_parsed()

                # Token page
                if url.netloc == 'api.vk.com':
                    state = 'get_token'
                    continue

                # Error page, try to repeat with empty cookies
                elif 'err' in url.path:
                    log_message('cookies corrupted, trying to repeat...')

                    self.http.clear_cookies()
                    state = 'auth_page'
                    continue

                else:
                    # TODO: fix the ugly parsing
                    doc = lxml.html.document_fromstring(
                        self.http.text().encode('utf-8'))
                    form = doc.forms[0]
                    action_url = urlparse(form.action)
                    act = parse_qs(action_url.query)['act'][0]

                    if act == 'login' or act == 'grant_access':
                        state = act
                        continue
                    else:
                        print('#Error: unpredictable behavior 1')
                        quit()

            # Form with login and password
            # Password is asked from `stdin' due to security reasons
            #
            # `doc' and `action_url' and `act' variables are passed
            # from `auth_page' state
            elif state == 'login':

                # Collect post data from the form and fill user-defined fields
                post_data = dict(doc.forms[0].fields)
                post_data['email'] = self.username
                post_data['pass'] = user_interaction.ask_pw()

                self.http.set_url(form.action)
                self.http.set_post_param(post_data)

                self.http.req_post()

                doc = lxml.html.document_fromstring(
                    self.http.text().encode('utf-8'))

                # Check for wrong password
                errors = doc.find_class('service_msg_warning')
                if len(errors) > 0:
                    print('#Error: email or password may be wrong')
                    # TODO: print error text from page
                    continue

                url = self.http.url_parsed()

                # Token page
                if url.netloc == 'api.vk.com':
                    state = 'get_token'
                    continue

                # Otherwise: check the need to confirm access
                form = doc.forms[0]
                action_url = urlparse(form.action)
                act = parse_qs(action_url.query)['act'][0]

                if act == 'grant_access':
                    state = act
                    continue
                else:
                    print('#Error: unpredictable behavior 2')
                    quit()

            # Form confirming access information
            elif state == 'grant_access':

                self.http.set_url(form.action)
                self.http.req_post()

                url = self.http.url_parsed()

                # Token page
                if url.netloc == 'api.vk.com':
                    state = 'get_token'
                    continue
                else:
                    print('#Error: unpredictable behavior 3')
                    quit()

            elif state == 'get_token':
                assert isinstance(url, ParseResult)

                # Final token
                token = parse_qs(url.fragment)['access_token'][0]

                # Prepare cache for cookies and token
                cache['API_TOKEN'] = token
                cache['API_TOKEN_TIME'] = int(time.time())
                cache['API_MASK'] = self.mask
                cache.set_packed('API_COOKIES', cookies)

                # Write to cache file
                cache.write()

                return token

    ## Auxillary methods

    # Check the given token for validity by a simple API request
    def check_token(self, token):
        tmp = self.token
        self.token = token
        test = self.req('isAppUser', error_handling=False)
        self.token = tmp
        return True if 'error' not in test else False

    # Convert set with categories of permissions to numerical access mask
    def access_mask(self, categories):
        mask = 0
        for cat in categories:
            mask += settings.masks[cat]
        return mask
