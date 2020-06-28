# -*- coding: utf-8 -*-
"""
    pyvk.constants
    ~~~~~~~~~~~~~~

    VK API related constants

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""


# Access Rights
p_notify = 1
p_friends = 2
p_photos = 4
p_audio = 8
p_video = 16
p_questions = 64
p_stories = 64
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


p_all = (
    p_notify
    | p_friends
    | p_photos
    | p_audio
    | p_video
    | p_stories
    | p_pages
    | p_leftmenu
    | p_status
    | p_notes
    | p_messages
    | p_wall
    | p_ads
    | p_offline
    | p_docs
    | p_groups
    | p_notifications
    | p_stats
    | p_email
    | p_market
)


p_basic = (
    p_friends | p_photos | p_audio | p_video | p_status | p_messages | p_wall | p_groups | p_offline
)


# Error Codes
E_TOO_MANY = 6
E_FLOOD = 9
E_CAPTCHA = 14
