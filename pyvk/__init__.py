# -*- coding: utf-8 -*-
"""
    pyvk
    ~~~~

    VK API for Python

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""


from .api import API
from .auth import ClientAuth, ServerAuth
from . import constants
from . import exceptions

globals().update({k: v for k, v in constants.__dict__.items()
                  if k.startswith('p_')})
