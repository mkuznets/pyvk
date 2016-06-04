# -----------------------------------------------------------------------------
# pyvk: settings.py
#
# Global parameters for network requests and user data storage.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------


global_options = {
    'timeout': 6.05,
    'version': '5.52',
}


ui_options = {
    'auto_reauth': True,
    'slow_down': False,
    'max_attempts': 5,
}


req_options = {
    'error_handling': True,

    # Unused
    'user_agent': 'Mozilla/5.0(Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


auth_options = {
    'disable_cache': False,
}


from .utils import PY2, PY3

if not PY2:
    from collections import ChainMap

def options(module):

    if PY2:
        opt = global_options.copy()
        opt.update(globals()[module + '_options'])
        return opt.items()
    else:
        return ChainMap({}, global_options, globals()[module + '_options']).items()
