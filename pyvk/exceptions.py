# -*- coding: utf-8 -*-
"""
    pyvk.exceptions
    ~~~~~~~~~~~~~~~

    Implements custom exceptions.

    :copyright: (c) 2013-2016, Max Kuznetsov
    :license: MIT, see LICENSE for more details.
"""


from __future__ import generators, with_statement, print_function, \
    unicode_literals, absolute_import


class PyVKError(Exception):

    def __init__(self, err_text, **attrs):
        self.err_text = err_text
        self.attrs = attrs

    def __str__(self):
        args_text = "\n".join("  %s: %s" % (k, repr(v)) for k, v in self.attrs.items())
        return "%s\nRelated attrs:\n%s" % (self.err_text, args_text)

    def __getattr__(self, name):
        return self.attrs[name]


class AuthError(PyVKError):
    pass


class ReAuthNeeded(PyVKError):
    pass


class ReqError(PyVKError):
    pass


class APIError(PyVKError):
    pass
