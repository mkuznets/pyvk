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
    def prompt(prompt):
        return input(prompt).strip()

    @staticmethod
    def ask(field, **kwargs):

        if field == 'username':
            return Prompt.prompt('Username (email of mobile number): ')

        elif field == 'api_id':
            return Prompt.prompt('API ID: ')

        elif field == 'password':
            return getpass.getpass('Password: ')

        elif field == 'secret_code':
            return Prompt.prompt('Secret code: ')

        elif field == 'phone':
            try:
                return Prompt.prompt('%s: ' % kwargs['msg'])
            except KeyError:
                raise ValueError('Message is not provided')

        elif field == 'captcha':
            try:
                text = "%s\nEnter text from the picture above" % kwargs['img']
                return Prompt.prompt('Secret code: ')
            except KeyError:
                raise ValueError('Image URL is not provided')
