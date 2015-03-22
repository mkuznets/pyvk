#!/usr/bin/env python3

import sys
import settings
import requests
import lxml.html
from urllib.parse import urlparse, ParseResult, parse_qs

class browser:

    def __init__(self):
        self._scheme = ''
        self._server = ''
        self._path = ''
        self._get_param = {}
        self._post_param = {}
        self._cookies = {}
        self._allow_redirects = True
        self._timeout = settings.http_timeout
        self._headers = {
            'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64; rv:22.0) ' +
                          'Gecko/20100101 Firefox/22.0',
        }

        self._result = None

    # Getters and setters
    def set_url(self, url):
        url_parts = urlparse(url)
        self._scheme = url_parts.scheme
        self._server = url_parts.netloc
        self._path = url_parts.path
        self._fragment = url_parts.fragment

        self._get_param = \
            {n: v[0] for(n, v) in parse_qs(url_parts.query).items()}

    def set_scheme(self, scheme):
        self._scheme = scheme

    def set_server(self, server):
        self._server = server

    def set_path(self, path):
        self._path = path

    def set_get_param(self, get_param):
        self._get_param = get_param

    def set_get_param_from_qs(self, qs):
        self._get_param = {name: value[0]
                           for(name, value) in parse_qs(qs).items()}

    def set_post_param(self, post_param):
        self._post_param = post_param

    def set_cookies(self, cookies):
        self._cookies = cookies

    def clear_cookies(self):
        self._cookies = {}

    def allow_redirects_on(self):
        self._allow_redirects = True

    def allow_redirects_off(self):
        self._allow_redirects = False

    # HTTP requests
    def req_get(self):
        self._req('get')

    def req_post(self):
        self._req('post')

    def _req(self, method):

        state = ''

        try:
            while state != 'exit':
                requests_methods = {'get': requests.get, 'post': requests.post}

                self._result = requests_methods[method](
                    self._scheme + '://' + self._server + self._path + '#' + self._fragment,
                    params=self._get_param,
                    data=self._post_param,
                    cookies=self._cookies,
                    headers=self._headers,
                    timeout=self._timeout,
                    allow_redirects=False)

                # Collect cookies
                for(name, value) in self._result.cookies.items():
                    self._cookies[name] = value

                # Cleanup post data
                self.set_post_param({})

                if self._allow_redirects:
                    if 'location' in self.headers():
                        self.set_url(self.headers()['location'])
                        method = 'get'
                        continue
                    else:
                        state = 'exit'

        except requests.exceptions.RequestException as e:
            print("Network error:\n" + str(e))
            sys.exit(2)

    # Get response data
    def text(self):
        return self._response('text')

    def json(self):
        return self._response('json')

    def binary(self):
        return self._response('bin')

    def headers(self):
        return self._response('headers')

    def url(self):
        return self._response('url')

    def url_parsed(self):
        return self._response('url_parsed')

    def _response(self, content):
        assert isinstance(self._result, requests.models.Response)
        if content == 'json':
            return self._result.json()

        contents = {'text': self._result.text,
                    'headers': self._result.headers,
                    'url': self._result.url,
                    'url_parsed': urlparse(self._result.url),
                    'bin': self._result.content}
        return contents[content]
