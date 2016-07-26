# -----------------------------------------------------------------------------
# pyvk: settings.py
#
# Global parameters for network requests and user data storage.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------

import logging


p_notify = 1
p_friends = 2
p_photos = 4
p_audio = 8
p_video = 16
p_offers = 32
p_questions = 64
p_pages = 128
p_leftmenu = 256
p_status = 1024
p_notes = 2048
p_messages = 4096
p_wall = 8192
p_ads = 32768
p_offline = 65536
p_docs = 131072
p_groups = 262144
p_notifications = 524288
p_stats = 1048576
p_email = 4194304
p_market = 134217728


p_all = p_notify | p_friends | p_photos | p_audio | p_video \
    | p_offers | p_questions | p_pages | p_leftmenu | p_status \
    | p_notes | p_messages | p_wall | p_ads | p_offline | p_docs \
    | p_groups | p_notifications | p_stats | p_email | p_market


p_basic = p_friends | p_photos | p_audio | p_video | p_status | p_messages \
    | p_wall | p_groups


global_options = {
    'log_format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
    'log_level': logging.INFO,
    'log_file': None,
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
    'scope': p_basic,
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
