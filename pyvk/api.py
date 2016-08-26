"""
    pyvk.api
    ~~~~~~~~

    Defines classes for VK API public interface, requests, and authorisation.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""


from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

from time import sleep
import logging

from . import settings
from .auth import Auth
from .exceptions import APIError, ReqError, AuthError
from .request import Request
from .utils import Prompt, Continuation


logger = logging.getLogger(__name__)


class API(object):

    def __init__(self, api_id, **kwargs):

        for name, default in settings.options('ui'):
            setattr(self, name, kwargs.get(name, default))

        log_file = {'filename': self.log_file} if self.log_file else {}
        logging.basicConfig(format=self.log_format, level=self.log_level,
                            **log_file)

        self.prompt = kwargs.get('prompt', Prompt)

        self.auth = Auth(api_id, **kwargs)
        if not self.auth.token:
            self.auth.auth()

    def __getattr__(self, attr):
        return Continuation(self.req, attr)

    def __repr__(self):
        return '<VK:%d>' % self.auth.api_id

    def __str__(self):
        return self.__repr__()

    def req(self, method, **args):

        args['access_token'] = self.auth.token
        args['v'] = args.get('v', self.version)

        r = Request(method, args)

        for attempt in range(self.max_attempts):
            try:
                return r.run()

            except APIError as e:

                if (e.code == 5 or e.code == 10) and self.auto_reauth:
                    # User authorisation failed, try to reauthorise.
                    logger.info('It seems that current token is unavailable '
                                'now. Trying to renew...')
                    try:
                        self.auth.auth()

                    except AuthError as e:
                        raise ReqError('Could not renew token',
                                       exc=e, attempt=attempt)

                    else:
                        assert self.auth.token
                        r.args['access_token'] = self.auth.token

                        logger.info('Access token succesfully renewed, '
                                    'repeating the request...')

                elif e.code in (6, 9):
                    # Requests are too ofter.
                    t = 0.3 * (attempt + 1)
                    logger.info('Too many requests per second. '
                                'Wait %.1f sec and retry.' % t)
                    sleep(t)

                elif e.code == 14:
                    # Captcha needed.

                    try:
                        args['captcha_sid'] = e.error['captcha_sid']
                        img = e.error['captcha_img']

                    except KeyError:
                        raise ReqError('Captcha is required, server response'
                                       'is malformed', exc=e)

                    else:
                        key = self.prompt.ask_captcha(img)
                        args['captcha_key'] = key

                else:
                    # Don't handle the error, raise it as is.
                    raise

        else:
            raise ReqError('Request failed after all attempts.')
