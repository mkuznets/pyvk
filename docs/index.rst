PyVK
====

**PyVK** is a Python client to `VK API`_.
It can be used in server or client applications, scripts, or interactively for
data retrieval and analysis, social media integration, automation, and fun.

.. _VK API: https://vk.com/dev/

Features
--------

* **Authorisation:** PyVK assists both client- and server-side authorisation.
  It ensures that your password is not stored anywhere in plain-text.
  It also supports 2FA and captcha/mobile phone login confirmation.
* **Error handling:** PyVK wraps API errors into exceptions and can recover
  from certain kinds of those, such as expired autorisation, temporal ban,
  or captcha request.
* **Pagination:** PyVK can join paginated API responses into a single result.
* **Media upload:** PyVK wraps it into a single method call
  and makes it easy to use those files as attachments in other API calls.
* **Python 2 and 3 :** PyVK is tested for CPython 2.7 and 3.5-3.8

Example
-------

.. code-block:: python

    >>> from pyvk import ClientAuth

    >>> auth = ClientAuth(app_id=<...>, username=<...>)
    >>> auth.auth()
    Password: <...>
    >>> api = auth.api(version='5.21', lang='en')

    >>> # Call API methods
    >>> api.users.get(user_ids=[210700286], fields=['bdate'])
    [{'id': 210700286,
      'first_name': 'Lindsey',
      'last_name': 'Stirling',
      'bdate': '21.9.1986'}]

.. _authorisation:

Authorisation
-------------

PyVK supports two types of authorisation:

* **Client-Side** (so-called \"`Implicit`_\") flow
  is suitable for interactive sessions and applications with a user interface.
  In this mode a user provides their login/password directly to PyVK:
* **Server-Side** (so-called \"`Authorisation code`_\") flow
  is intended for long-running server scripts, web-services,
  and other applications where there is no or limited user interaction.

.. _Authorisation code: https://vk.com/dev/implicit_flow_user
.. _Implicit: https://vk.com/dev/implicit_flow_user


Client-Side
+++++++++++

.. py:class:: pyvk.ClientAuth(app_id=None, username=None, [**options])

    Client-side auth object. In this mode a user provides their login/password directly to PyVK.

    .. code-block:: python

        >>> auth = ClientAuth(app_id=<...>, username=<...>)
        >>> auth.auth()
        Password: <...>

    The password is requested only once and not stored anywhere.
    PyVK remembers the access token and session cookies so that
    next time the authorisation will succeed immediately.

    Apart from password PyVK may also request
    2FA code, mobile number, and captcha
    depending on the situation and your profile settings.
    By default the input is read from stdin. One can also implement other
    ways of getting the input if the application is not supposed to have
    a shell session.
    Refer to :py:attr:`~.config.GlobalConfig.input` and :ref:`user-input`
    for more details.

    :param app_id: VK application identifier.
                   Will be requested via an interactive session
                   if not specified.
    :param username: VK login (email, username, or mobile phone).
                     Will be requested via an interactive session
                     if not specified.
    :param [options]: custom values for :ref:`global-config`
                      and :ref:`client-auth-config` configuration options.
                      The latter ones are applied automatically
                      to API objects spawned by :py:meth:`~.ClientAuth.api`.

    .. py:attribute:: token

        VK API token.
        Initialised only if authorisation is complete.

    .. py:attribute:: scope

        Bitmask of access rights.
        Initialised only if authorisation is complete.

    .. py:method:: auth()

        Starts authorisation.
        Initialises :py:attr:`~.ClientAuth.token`
        and :py:attr:`~.ClientAuth.scope` attributes if successful.

        :raises AuthError: if authorisation is unsuccessful.

    .. py:method:: api([**options])

        Returns an :py:class:`~pyvk.API` object if authorised.

        :param [options]: custom values for :ref:`global-config`
                          and :ref:`api-config` configuration options.
                          The latter ones given to auth objects
                          apply automatically.
        :raises AuthError: if not authorised
        :returns: :py:class:`~pyvk.API` object

Server-Side
+++++++++++

In this mode a user should be redirected to VK login page:

  .. code-block:: python

    >>> from pyvk import ServerAuth, p_photos, p_audio
    >>> auth = ServerAuth(app_id=<...>,
                          redirect_uri='https://<example-server>/vkauth')
    >>> auth.auth_url
    'https://oauth.vk.com/authorize?client_id=[...]&response_type=code'

Once the user granted permissions to your application,
VK API sends a unique code to the callback URL to complete the authorisation:

  .. code-block:: python

    >>> # App Server
    >>> # GET /vkauth?code=<...>
    >>> auth = ServerAuth(<...>)  # (same as at the first step)
    >>> auth.auth(
    ...     code=<...>,           # `code' from the query string
    ...     client_secret=<...>   # from VK application settings
    ... )



.. py:class:: pyvk.ServerAuth(app_id, redirect_uri, [**options])

    Server-side auth helper. It is intended for long-running server scripts,
    web-services, and other applications where there is no or limited
    user interaction.
    See official VK documentation on `Authorisation Code Flow
    <https://vk.com/dev/authcode_flow_user>`__
    for low-level details.

    Intended workflow:

    * Redirect user to login page URL given by :py:attr:`.auth_url`
    * If user confirms access for application,
      they will be redirected to `redirect_uri`
    * Pass `code` (from query string)
      and `client_secret` (from application settings) values
      to :py:meth:`~.ServerAuth.auth`
    * Authorisation is complete.
      Now you can put :py:attr:`~.ServerAuth.token` into persistent storage
      and use it to create API objects if needed.

    :param app_id: VK application identifier.
    :param redirect_uri: callback URL that is requested by VK API to send
                         a secret code which is then used by the sever to
                         request an access token.
    :param [options]: custom values for :ref:`global-config`
                      and :ref:`server-auth-config` configuration options.
                      The latter ones are applied automatically
                      to API objects spawned by :py:meth:`~.ServerAuth.api`.


    .. py:attribute:: token

        VK API token.
        Initialised only if authorisation is complete.

    .. py:attribute:: scope

        Bitmask of access rights. Ditto.

    .. py:attribute:: auth_url

        URL for the first step of authorisation

    .. py:method:: auth(code, client_secret)

        Completes authorisation with `code` and `client_secret` provided by VK
        via GET request to `redirect_uri`.
        Initialises :py:attr:`~.ServerAuth.token`
        and :py:attr:`~.ServerAuth.scope` attributes if successful.

        :param code: parameter from GET request sent to `redirect_uri`
        :param client_secret: secret key from VK application settings
        :raises AuthError: if authorisation is unsuccessful.

    .. py:method:: api([**options])

        Returns an :py:class:`~pyvk.API` object if authorised.

        :param [options]: custom values for :ref:`global-config`
                          and :ref:`api-config` configuration options.
                          The latter ones given to auth objects
                          apply automatically.
        :raises AuthError: if not authorised
        :returns: :py:class:`~pyvk.API` object



Usage
-----

VK API is accessible via :py:class:`.API` object.
There are three ways to get one:

* From an :ref:`auth object <authorisation>`.
  This is particulary handy for client applications:

  .. code-block:: python

        >>> auth = ClientAuth(app_id=<...>, username=<...>)
        >>> auth.auth()
        Password: <...>
        >>> api = auth.api()

  Keyword parameters given to :py:meth:`~.ClientAuth.api` will be passed to
  the :py:class:`.API` constructor. :ref:`Global parameters <global-config>`
  will be inherited from the auth object (if not shadowed).

* In server applications an auth object may not be around
  when it feels like an API call.
  In this case one can store an access token persistently and then use it
  create an :py:class:`.API` object manually:

  .. code-block:: python

        >>> auth = ServerAuth(<...>)
        >>> auth.auth(code=<...>, client_secret=<...>)
        >>> db['token'] = auth.token

        >>> # Elsewhere, elsewhen:
        >>> from pyvk import API
        >>> api = API(token=db['token'])

* While it is not really common in practice,
  one can use a handful of API methods without an access token at all:

  .. code-block:: python

        >>> api = API()
        >>> api.users.getFollowers(user_id=1, count=1)
        {'count': 5985409, 'items': [354451485]}


.. py:class:: pyvk.API([token], [**parameters])

    :param str token: authorisation token. If `None`, only a small part of
                      VK API methods is available.)


If you have obtained an API token elsewhere, you can use it directly:

.. code-block:: python

    >>> from pyvk import API
    >>> api = API(token=<...>)


API Calls
+++++++++

Let's call a couple of `VK API methods`_:

.. _VK API methods: https://vk.com/dev/methods

.. code-block:: python

    >>> api.users.get(user_ids=[210700286], fields=['bdate'])
    [{'bdate': '21.9.1986',
      'first_name': 'Lindsey',
      'id': 210700286,
      'last_name': 'Stirling'}]

Or, without fancy attribute-chaining:

.. code-block:: python

    >>> vk.call('account.getInfo')
    {'2fa_required': 0,
     'country': 'RU',
     'https_required': 0,
     'intro': 0,
     'lang': 0,
     'no_wall_replies': 0,
     'own_posts_default': 0}


Note that pythonic integers and lists can be used
where the official API documentation specifies
numbers (including negative)
and comma-separated lists.

Error Handling
++++++++++++++

VK API errors can be catched as exceptions:

.. code-block:: python

    >>> from pyvk.exceptions import APIError
    >>> try:
    ...     api.docs.get()
    ... except APIError as exc:
    ...     print('Error %d: %s' % (exc.error_code, exc.error_msg))

    Error 15: Access denied: no access to call this method

However, PyVK can handle some recoverable errors
("too many requests per second", "captcha needed", and the like)
by its own:

.. code-block:: python

    >>> for i in range(1, 100000):
    ...     api.users.get(user_ids=[i])
    ...     print(i, end=' ')
    ...     sys.stdout.flush()
    1 2 3 4 5 6 7 8 9 10 11 12 13 14 <...> pyvk.request INFO: Too many requests per second. Wait 0.3 sec and retry.
    <...> pyvk.request INFO: Too many requests per second. Wait 0.6 sec and retry.
    <...> pyvk.request INFO: Too many requests per second. Wait 1.2 sec and retry.
    15 16 17 18 19 20 <...>


If that is not what you want, just make your request handler a bit dumber:

.. code-block:: python

    >>> api = auth.api(auto_delay=False, validation=False)

Or pass ``raw=True`` to work with JSON responses directly:

.. code-block:: python

    >>> api = auth.api(raw=True)
    >>> api.docs.get()
    {'error': {'error_code': 15, 'error_msg': 'Access denied: no access to call this method', <...>}}

Configuration
-------------

Access Rights
+++++++++++++

VK API requires an `access control bitmask`_ passed during authorisation.
PyVK provides bitmasks for individual access rights as package-level constants.
They can be combined by bitwise-or operator and passed
into :py:class:`.ClientAuth` or :py:class:`.ServerAuth` with `scope` argument:

.. _access control bitmask: https://vk.com/dev/permissions

.. code-block:: python

    >>> from pyvk import p_audio, p_offline
    >>> auth = ClientAuth(app_id=<...>, username=<...>,
                          scope=p_audio | p_offline)

There are also predefined :py:data:`~pyvk.p_all` and :py:data:`~pyvk.p_basic`.
The latter is used by default in :py:class:`.ClientAuth` and combines
access rights commonly used used in scripts and interactive sessions.
:py:class:`.ServerAuth` defaults to :py:data:`~pyvk.p_offline`.

.. py:data:: pyvk.p_basic

    Combines :py:data:`~pyvk.p_friends`,
    :py:data:`~pyvk.p_photos`, :py:data:`~pyvk.p_audio`,
    :py:data:`~pyvk.p_video`, :py:data:`~pyvk.p_status`,
    :py:data:`~pyvk.p_messages`, :py:data:`~pyvk.p_wall`,
    :py:data:`~pyvk.p_groups`, :py:data:`~pyvk.p_offline`.

.. py:data:: pyvk.p_all

    Combines all the access rights.

.. py:data:: pyvk.p_notify

    User allowed to send notifications to they (for Flash/iFrame apps)

.. py:data:: pyvk.p_friends

    Access to friends.

.. py:data:: pyvk.p_photos

    Access to photos.

.. py:data:: pyvk.p_audio

    Access to audio.

.. py:data:: pyvk.p_video

    Access to video.

.. py:data:: pyvk.p_pages

    Access to wiki pages.

.. py:data:: pyvk.p_leftmenu

    Addition of link to the application in the left menu.

.. py:data:: pyvk.p_status

    Access to user status.

.. py:data:: pyvk.p_notes

    Access to notes.

.. py:data:: pyvk.p_messages

    Access to advanced methods for messaging.
    Unavailable for server-side authorisation.

.. py:data:: pyvk.p_wall

    Access to standard and advanced methods for the wall.
    Ignored for server-side authorisation.

.. py:data:: pyvk.p_ads

    Access to advanced methods for `Ads API <https://vk.com/dev/ads>`__.

.. py:data:: pyvk.p_offline

    Access to API at any time (non-expiring access token).

.. py:data:: pyvk.p_docs

    Access to docs.

.. py:data:: pyvk.p_groups

    Access to user communities.

.. py:data:: pyvk.p_notifications

    Access to notifications about answers to the user.

.. py:data:: pyvk.p_stats

    Access to statistics of user groups and applications
    where they is an administrator.

.. py:data:: pyvk.p_email

    Access to user email.

.. py:data:: pyvk.p_market

    Access to market.

.. _user-input:

User Input
++++++++++

.. autoclass:: pyvk.Input
    :members:

Options
+++++++

The following are configuration options and their default value used by
:py:class:`.ClientAuth`, :py:class:`.ServerAuth`, and :py:class:`.API`.
Global options apply to all the classes, the others are specific to
certain class.
One can customise them by passing corresponding keyword arguments
when constructing the objects in question, for example:

.. code-block:: python

    >>> auth = ClientAuth(app_id=<...>, username=<...>, timeout=20.05,
                          version='5.0', disable_cache=True)

    >>> auth = ServerAuth(app_id=<...>, username=<...>,
                          log_file='/logs/auth.log',
                          scope=p_groups | p_notes)

    >>> api = API(token=<...>, scope=p_docs, lang='ru', max_attempts=10)


.. _global-config:

Global
......

.. autoclass:: pyvk.config.GlobalConfig
   :members:

.. _client-auth-config:

ClientAuth
..........

.. autoclass:: pyvk.config.ClientAuthConfig
   :members:

.. _server-auth-config:

ServerAuth
..........

.. autoclass:: pyvk.config.ServerAuthConfig
   :members:


.. _api-config:

API
...

.. autoclass:: pyvk.config.APIConfig
    :members:
