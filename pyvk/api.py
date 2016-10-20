# -*- coding: utf-8 -*-
"""
    pyvk.api
    ~~~~~~~~

    Defines classes for VK API public interface, requests, and authorisation.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""

from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import

import logging

from .config import GlobalConfig, AuthConfig, RequestConfig
from .auth import Auth
from .request import RequestHandler

logger = logging.getLogger(__name__)


class API(object):
    def __init__(self, **kwargs):
        self.config = GlobalConfig(**kwargs)

        log_file = {'filename': self.config.log_file} \
            if self.config.log_file else {}
        logging.basicConfig(format=self.config.log_format,
                            level=self.config.log_level,
                            **log_file)
        # Singleton
        self.auth = Auth(AuthConfig(**kwargs))

        if not self.auth.token:
            self.auth.auth()

    def get_handler(self, **kwargs):
        return RequestHandler([], self.auth, RequestConfig(**kwargs))

    def __repr__(self):
        return '<VK API | id=%d>' % self.auth.api_id
