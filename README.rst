-----------------
VK API for Python
-----------------

.. image:: https://travis-ci.org/mkuznets/pyvk.svg?branch=master
    :target: https://travis-ci.org/mkuznets/pyvk

.. image:: https://coveralls.io/repos/github/mkuznets/pyvk/badge.svg?branch=master
    :target: https://coveralls.io/github/mkuznets/pyvk?branch=master

.. image:: https://img.shields.io/pypi/v/pyvk.svg?style=flat
    :target: https://pypi.python.org/pypi/pyvk

`VK`_ is one of the major Russian-speaking social networks.
**PyVK** is a no-nonsence boilerplate-free `VK API`_ library for Python.
It can be used in server or client applications, scripts, or interactively for
data retrieval and analysis, social media integration, automation, and fun.

.. _VK: https://vk.com
.. _VK API: https://vk.com/dev/


Quickstart
----------

Authorisation
=============

PyVK supports two types of authorisation:

* **Client-Side** (\"`Implicit`_\") flow
  is suitable for interactive sessions and applications with a user interface.
  In this mode a user provides their login/password directly to PyVK:

  .. _Implicit: https://vk.com/dev/implicit_flow_user

  .. code-block:: python

    >>> from pyvk import ClientAuth
    >>> auth = ClientAuth(api_id=<...>, username=<...>)
    >>> auth.auth()
    Password: <...>

  The password is requested only once.
  PyVK remembers the access token and session cookies so that
  next time the authorisation will succeed immediately.
  This ensures that your password is not stored anywhere in plain-text.
  PyVK may also request 2FA code, mobile number, and/or captcha
  depending on your profile settings.

  By default PyVK reads the information from the standard input.
  You can also define custom credential providers if your application
  is not supposed to have a shell session.
* **Server-Side** (\"`Authorisation code`_\") flow
  is intended for long-running server scripts, web-services,
  and other applications where there is no or limited user interaction.
  In this mode a user should be redirected to VK login page:

  .. _Authorisation code: https://vk.com/dev/implicit_flow_user

  .. code-block:: python

    >>> # User Interface
    >>> from pyvk import ServerAuth, p_photos, p_audio
    >>> auth = ServerAuth(api_id=<...>, redirect_uri='https://<example-server>/vkauth')
    >>> auth.auth_url
    'https://oauth.vk.com/authorize?client_id=<...>&display=page[...]&response_type=code'

  Once the user granted permissions to your application,
  VK API sends a unique code to the callback URL to complete the authorisation:

  .. code-block:: python

    >>> # App Server
    >>> # GET /vkauth?code=<...>
    >>> auth = ServerAuth(<...>)  # (same as at the first step)
    >>> auth.auth(
    ...     code=<...>,           # `code' from the query string
    ...     client_secret=<...>   # secret key from VK application settings
    ... )

Either way,
the access rights are configured by passing a desired `access bitmask`_
with a ``scope`` argument.

.. _access bitmask: https://vk.com/dev/permissions

.. code-block:: python

    >>> from pyvk import p_audio, p_offline
    >>> api = ClientAuth(api_id=<...>, username=<...>, scope=p_audio | p_offline)

By default ``p_basic`` is used for ``ClientAuth``. It gives a
non-expiring access to friends, photos, audio/video, messages, wall, and groups.
``p_offline`` is a default for ``ServerAuth``.


``API`` Object
==============

Once authorised, get youself an ``API`` object.
A default one may be good enough for you:

.. code-block:: python

    >>> vk = auth.get_api()

Or you can customise it with
global API settings, request parameters, and error handling options:

.. code-block:: python

    >>> vk = auth.get_api(version='5.21', lang='en', max_attempts=10, timeout=30.)

If you have obtained an API token elsewhere, you can use it directly:

.. code-block:: python

    >>> from pyvk import API
    >>> vk = API(token=<...>)

Frankly, for some VK API methods you do not even need the token:

.. code-block:: python

    >>> vk = API()


API Calls
=========

Let's call a couple of `VK API methods`_:

.. _VK API methods: https://vk.com/dev/methods

.. code-block:: python

    >>> vk.users.get(user_ids=[210700286], fields=['bdate'])
    [{'first_name': 'Lindsey', 'last_name': 'Stirling', 'id': 210700286, 'bdate': '21.9.1986'}]

    >>> pprint(vk.audio.search(q='The Beatles - Let It Be', count=1))
    {'count': 18006,
     'items': [{'artist': 'The Beatles',
                'date': 1308179559,
                'duration': 243,
                'genre_id': 1,
                <...>
                'title': 'Let It Be',
                'url': 'https://cs9-15v4.vk.me/<...>'}]}

Or, without fancy attribute-chaining:

.. code-block:: python

    >>> vk.call('account.getInfo')
    {'own_posts_default': 0, 'country': 'GB', 'intro': 0, 'no_wall_replies': 0, 'https_required': 1, 'lang': 3}

Note that pythonic integers and lists can be used
where the official API documentation specifies
numbers (including negative)
and comma-separated lists.

Error Handling
==============

VK API errors can be catched as exceptions:

.. code-block:: python

    >>> from pyvk.exceptions import APIError
    >>> try:
    ...     vk.docs.get()
    ... except APIError as err:
    ...     print('Error %d: %s' % (err.attrs['code'], err.attrs['msg']))

    Error 15: Access denied: no access to call this method

However, PyVK can handle some recoverable errors
("too many requests per second", "captcha needed", and the like)
by its own:

.. code-block:: python

    >>> for i in range(1, 100000):
    ...     vk.users.get(user_ids=[i])
    ...     print(i, end=' ')
    ...     sys.stdout.flush()
    1 2 3 4 5 6 7 8 9 10 11 12 13 14 <...> pyvk.request INFO: Too many requests per second. Wait 0.3 sec and retry.
    <...> pyvk.request INFO: Too many requests per second. Wait 0.6 sec and retry.
    <...> pyvk.request INFO: Too many requests per second. Wait 0.9 sec and retry.
    15 16 17 18 19 20 <...>


If that is not what you want, just make your request handler a bit dumber:

.. code-block:: python

    >>> vk = api.get_handler(slow_down=False, validation=False)

Or pass ``raw_response=True`` to work with JSON responses directly:

.. code-block:: python

    >>> vk = api.get_handler(raw_response=True)
    >>> vk.docs.get()
    {'error': {'error_code': 15, 'error_msg': 'Access denied: no access to call this method', <...>}}




Credits
-------

The idea of first-class queryset-like method calls
is inspired by `vk-requests`_.

.. _vk-requests: https://github.com/prawn-cake/vk-requests