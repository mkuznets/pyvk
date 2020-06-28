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
from .utils import Input
from .constants import *
from . import exceptions

__version__ = "0.1.2"
