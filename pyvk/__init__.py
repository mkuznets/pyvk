# -----------------------------------------------------------------------------
# pyvk: __init__.py
#
# Package file.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------


from .api import API
from . import settings

globals().update({k: v for k, v in settings.__dict__.items()
                  if k.startswith('p_')})
