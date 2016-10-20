-----------------
VK API for Python
-----------------

`VK`_ is one of the major Russian-speaking social networks.
**PyVK** is a no-nonsence boilerplate-free `VK API`_ library for Python.
It can be used in server or client applications, scripts, or interactively for
data retrieval and analysis, social media integration, automation, and fun.

.. _VK: https://vk.com
.. _VK API: https://vk.com/dev/


Usage
-----

Authorisation
=============

.. code-block:: python

    >>> from pyvk import API
    >>> api = API(api_id=<...>, username=<...>)
    Password: <...>

The password is requested only once:
PyVK caches an `API token`_ and renews it automatically.
This ensures that your password is not stored anywhere in plain-text.
Secret code, mobile phone, and captcha
may also be needed during authorisation depending on your profile settings.

.. _API token: https://vk.com/dev/access_token

By default PyVK reads the information from the standard input.
You can also define custom credential providers if your application
is not supposed to have an interactive shell session.

If you have obtained an API token elsewhere, you can use it directly.
Note that in this case PyVK will not renew the token when it is expired.

.. code-block:: python

    >>> api = API(token=<...>)

Access rights are configured by passing a desired `access bitmask`_
into a ``scope`` argument:

.. _access bitmask: https://vk.com/dev/permissions

.. code-block:: python

    >>> from pyvk import p_audio, p_wall, p_messages
    >>> api = API(api_id=<...>, username=<...>, scope=p_audio | p_wall | p_messages)

By default ``p_basic`` is used, it ensures an access to
friends, photos, audio/video, messages, wall, and groups.
Use ``p_all`` if you like to live dangerously.


Request Handler and Configuration
=================================

Once authorised, get a request handler. A default one is good enough:

.. code-block:: python

    >>> vk = api.get_handler()  # default handler

Handlers can be customised with
global API settings, request parameters, and error handling options:

.. code-block:: python

    >>> vk = api.get_handler(version='5.21', lang='en', max_attempts=10, timeout=30.)


API Calls
=========

Lets call a couple of `VK API methods`_:

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

Note that pythonic integers and lists can be used
where the official API documentation specify
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

    >>> vk = api.get_handler(auto_reauth=False, slow_down=False, validation=False)

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