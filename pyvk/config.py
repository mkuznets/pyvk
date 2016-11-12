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
from .utils import Input, Config, DictNamedTuple


class GlobalConfig(Config):
    # :param str log_format: the log messages format compatible with standard
    #                        `logging` module
    log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'

    # :param int log_level: the log messages level compatible with standard
    #                       `logging` module
    log_level = logging.INFO

    # :param log_file: optional log file. If not set, standard output is used
    # :type log_file: str or None
    log_file = None

    # :param input: static class for requesting user information during an
    #               interactive client session. `pyvk.Input` or its subclassed
    #               are expected.
    # type input: Input
    input = Input

    # :param float timeout: time for waiting for a network response
    timeout = 6.05

    # :param str version: VK API version. See official documentation for
    #                     version history and changelog
    version = '5.60'


class ServerAuthConfig(GlobalConfig):
    # :param app_id: VK application identifier
    # :type app_id: int or None
    app_id = None

    # :param int scope: bitmaks for access rights requested from VK API
    scope = p_offline

    # :param str redirect_uri: callback URL that is requested by VK API to send
    #                          a secret code which is then used by the sever to
    #                          request an access token
    redirect_uri = None

    # :param str display: a setting for the authorisation page appearance
    display = 'page'

    # :param state:	an arbitrary string that will be returned together with
    #               the authorisation result
    # :type state: str or None
    state = None


class ClientAuthConfig(GlobalConfig):
    # :param str app_id: VK application identifier. Will be requested via
    #                    an interactive session if not specified.
    # :type app_id: int or None
    app_id = None

    # :param int scope: bitmaks for access rights requested from VK API
    scope = p_basic

    # :param username: VK login (email, username, or mobile phone). Will be
    #                  requested via an interactive session if not specified
    # :type username: int or None
    username = None

    # :param bool disable_cache: controls authorisation cache. Is set, login
    #                            and password will be requested every time the
    #                            ClientAuth is called
    disable_cache = False


class APIConfig(GlobalConfig):
    # :param lang: language of VK API responses
    # :type lang: str or None
    lang = None

    # :param bool validation: if set, captcha requests will be handled via an
    #                         interactive session.
    validation = True

    # :param bool auto_delay: when encounter a request frequency limit, add
    #                         delays of increasing lenghts and repeat the
    #                         request `max_attempts` times.
    auto_delay = True

    # :param int max_attempts: how many times to repeat a failed request if the
    #                          failure is configured to be handled
    max_attempts = 5

    # :param bool raw: return raw response objects (converted from JSON) instead
    #                  of unpacking and error handling. If set, `validation` and
    #                  `auto_delay` will be ignored
    raw = False

    # :param Mapping response_type: an object used for JSON decoding. It defines
    #                               the type of map-like objects returned by
    #                               API calls.
    response_type = DictNamedTuple
