# -*- coding: utf-8 -*-
"""
    pyvk
    ~~~~

    VK API for Python

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""


from .api import API
from . import config
from . import exceptions

globals().update({k: v for k, v in config.__dict__.items()
                  if k.startswith('p_')})
