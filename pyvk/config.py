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
from .utils import Prompt, Config


class GlobalConfig(Config):
    log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'  # type: str
    log_level = logging.INFO    # type: int
    log_file = None             # type: str
    prompt = Prompt             # type: Prompt
    timeout = 6.05              # type: float
    version = '5.59'            # type: str
    user_agent = 'Mozilla/5.0(Windows NT 6.1; WOW64; rv:22.0) ' \
                 'Gecko/20100101 Firefox/22.0'  # type: str


class ServerAuthConfig(GlobalConfig):
    api_id = None           # type: int
    scope = p_offline       # type: int
    redirect_uri = None     # type: str
    display = 'page'        # type: str
    state = None            # type: str


class ClientAuthConfig(GlobalConfig):
    api_id = None           # type: int
    scope = p_basic         # type: int
    username = None         # type: str
    disable_cache = False   # type: bool


class APIConfig(GlobalConfig):
    lang = None           # type: str
    validation = True     # type: bool
    slow_down = True      # type: bool
    max_attempts = 5      # type: int
    raw_response = False  # type: bool
