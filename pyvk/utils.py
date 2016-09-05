# -*- coding: utf-8 -*-
"""
    pyvk.utils
    ~~~~~~~~~~

    Implements various utility classes and functions.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""

import getpass
import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:
    input = raw_input


class Prompt(object):

    @staticmethod
    def ask_text(prompt):
        return input(prompt).strip()

    @staticmethod
    def ask_username():
        return Prompt.ask_text('Username (email of mobile number): ')

    @staticmethod
    def ask_password():
        return getpass.getpass('Password: ')

    @staticmethod
    def ask_secret_code():
        return Prompt.ask_text('Secret code: ')

    @staticmethod
    def ask_captcha(img):
        text = "%s\nEnter text from the picture above" % img
        return Prompt.ask_text(text)
