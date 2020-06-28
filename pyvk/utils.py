# -*- coding: utf-8 -*-
"""
    pyvk.utils
    ~~~~~~~~~~

    Implements various utility classes and functions.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence

from inspect import getsourcelines
from itertools import takewhile
import getpass
import sys
import re


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:  # pragma: no cover
    from itertools import izip
    input = raw_input
    zip = izip
else:  # pragma: no cover
    zip = zip
    input = input


def accumulate(iterable):
    it = iter(iterable)

    try:
        total = next(it)
        yield total
    except StopIteration:
        return

    for element in it:
        total += element
        yield total


def filter_dict(d):
    # Remove None values
    return dict(filter(lambda x: x[1] is not None,
                       d.items()))


def process_args(args):

    def convert(item):
        if type(item) is list:
            # Transform lists into comma-separated strings
            return ','.join(str(x) for x in item)
        elif type(item) is bool:
            # Transform Booleans into 0 and 1
            return int(item)
        else:
            return item

    return filter_dict(dict((k, convert(v)) for k, v in args.items()))


def setup_logger(config):
    import logging
    log_file = {'filename': config.log_file} \
        if config.log_file else {}
    logging.basicConfig(format=config.log_format,
                        level=config.log_level, **log_file)


class DictNamedTuple(Mapping):

    def __init__(self, *args, **params):
        keys = []
        attrs = self.__dict__

        if args:
            source, = args

            if isinstance(source, Sequence):
                attrs.update(dict(source))
                keys.extend(k for k, v in source)

            elif isinstance(source, Mapping):
                attrs.update(source)
                keys.extend(source)

            else:
                raise TypeError("'%s' object is not iterable"
                                % type(source).__name__)

        keys.extend(set(params) - set(keys))
        attrs.update(params)

        attrs['_keys'] = tuple(keys)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            raise AttributeError("object has no attribute '%s'" % item)

    def __len__(self):
        return len(self.__dict__['_keys'])

    def __iter__(self):
        return (k for k in self.__dict__['_keys'])

    def __repr__(self):
        params = ', '.join('%s: %s' % (repr(k), repr(self[k])) for k in self)
        return '{{{params}}}'.format(params=params)

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        return dict(self) == dict(other)

    # Remove non-underscored methods as (1) they are not essential for most of
    # the desired dict-like behaviour (2) they may shadow user-defined keys.
    # NOTE: I admit it is really an abuse of the Mapping ABC. However this is
    # probably the easiest way to support things like (**container).
    items = None
    values = None
    get = None

    def __setattr__(self, attr, value):
        raise AttributeError('Cannot assign attributes to this class')


class Config(DictNamedTuple):

    def __init__(self, **params):

        new_params = {}

        classes = takewhile(lambda x: x is not DictNamedTuple,
                            self.__class__.__mro__)

        for cls in classes:
            for key, value in cls.__dict__.items():
                if not key.startswith('_'):
                    new_params[key] = params.get(key, value)

        super(Config, self).__init__(**new_params)

    def __repr__(self):
        params = ', '.join('%s=%s' % (k, repr(self[k])) for k in self)
        return '{name}({params})'.format(name=self.__class__.__name__,
                                         params=params)


class Input(object):
    """
    Interface for requesting input from user via stdin.
    One can subclass and override :py:meth:`~Input.ask` in order to
    implement other ways of providing the input.
    """

    @staticmethod
    def _prompt(prompt):
        return input(prompt).strip()

    @staticmethod
    def ask(field, **kwargs):
        """
        Read certain type of input from stdin with a relevant prompt.

        :param str field: type of input
        :return: input string
        :raises: ValueError if incorrect arguments are passed

        Additional keyword arguments are needed in some cases.

        Possible inputs:

        * ``ask('app_id')``
        * ``ask('username')``
        * ``ask('password')``
        * ``ask('secret_code')``
        * ``ask('phone', msg='...')``
        * ``ask('captcha', img='<image URL>')``
        """

        if field == 'username':
            return Input._prompt('Username (email of mobile number): ')

        elif field == 'app_id':
            return Input._prompt('API ID: ')

        elif field == 'password':
            return getpass.getpass('Password: ')

        elif field == 'secret_code':
            return Input._prompt('Secret code: ')

        elif field == 'phone':
            try:
                return Input._prompt('%s: ' % kwargs['msg'])
            except KeyError:
                raise ValueError('Message is not provided')

        elif field == 'captcha':
            try:
                text = "%s\nEnter text from the picture above: " % kwargs['img']
                return Input._prompt(text)
            except KeyError:
                raise ValueError('Image URL is not provided')

        else:
            raise ValueError('Unknown field')
