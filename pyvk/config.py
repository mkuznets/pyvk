# -*- coding: utf-8 -*-
"""
    pyvk.config
    ~~~~~~~~~~~~~

    Defines constants, parameters, and their default values.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""

import logging
from .constants import p_basic, p_offline
from .utils import Input, Config


class GlobalConfig(Config):
    #: log messages format compatible with :py:mod:`logging` module
    log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'

    #: log messages level compatible with :py:mod:`logging` module
    log_level = logging.INFO

    #: optional log file. If not set, standard output is used
    log_file = None

    #: static class for requesting user information during an
    #: interactive client session. :py:class:`.Input` or its subclassed
    #: are expected.
    input = Input

    #: time for waiting for a network response
    timeout = 6.05

    #: VK API version.
    #: See `version history <https://vk.com/dev/versions>`__
    #: for more information.
    version = '5.60'


class ServerAuthConfig(GlobalConfig):
    app_id = None
    redirect_uri = None

    #: bitmaks for access rights requested from VK API
    scope = p_offline

    #: sets authorisation page appearance.
    #: See `VK documentation <https://vk.com/dev/authcode_flow_user>`__
    #: for more details
    display = 'page'

    #: an arbitrary string that will be returned
    #: together with the authorisation result
    state = None


class ClientAuthConfig(GlobalConfig):
    app_id = None
    username = None

    #: bitmask for access rights requested from VK API
    scope = p_basic

    #: controls authorisation cache.
    #: If set, login and password will be requested
    #: every time ClientAuth is called
    disable_cache = False


class APIConfig(GlobalConfig):
    #: language of VK API responses
    lang = 'en'

    #: if set, captcha requests will be handled via an interactive session.
    validation = True

    #: when encounter a request frequency limit
    #: add delays of increasing lenghts and repeat the
    #: request `max_attempts` times.
    auto_delay = True

    #: how many times to repeat a failed request if the
    #: failure is configured to be handled
    max_attempts = 5

    #: return raw response objects (converted from JSON) instead
    #: of unpacking and error handling. If set, `validation` and
    #: `auto_delay` will be ignored
    raw = False

    #: an object used for JSON decoding. It defines
    #: the type of map-like objects returned by API calls.
    response_type = dict
