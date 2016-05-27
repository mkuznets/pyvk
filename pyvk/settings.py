# -----------------------------------------------------------------------------
# pyvk: settings.py
#
# Global parameters for network requests and user data storage.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------


timeout = 6.05

# TODO: use `appdirs' to choose correct config/cache directory on any platform.
import os
cache_dir = os.path.join(os.getenv('HOME'), '.pyvk/')

MAX_ATTEMPTS = 5

api_version = '5.37'

useragent = 'Mozilla/5.0(Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'
