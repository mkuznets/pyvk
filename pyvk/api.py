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

from .config import RequestConfig
from .auth import Auth
from .request import PartialRequest

logger = logging.getLogger(__name__)


class API(object):
    def __init__(self, api_id, **kwargs):
        self.config = RequestConfig(**kwargs)

        log_file = {'filename': self.config.log_file} \
            if self.config.log_file else {}

        logging.basicConfig(format=self.config.log_format,
                            level=self.config.log_level,
                            **log_file)

        self.auth = Auth(api_id, **kwargs)

        if not self.auth.token:
            self.auth.auth()

    def __getattr__(self, api_method_prefix):
        return PartialRequest([api_method_prefix],
                              {'config': self.config, 'auth': self.auth})

    def request(self, **kwargs):
        return PartialRequest([], {'config': RequestConfig(**kwargs),
                                   'auth': self.auth})

    def __repr__(self):
        return '<VK API | id=%d>' % self.auth.api_id
