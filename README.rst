-----------------
VK API for Python
-----------------

PyVK implements a Python client for `VK`_ (major Russian social network.) It is

.. _VK: https://vk.com

* **cross-platform:**
  Supports both Python 2 and 3.
* **user-friendly:**
  Robust authorisation. Error handling.
* **smart:**
  Renews expired authorisation.
  Repeats failed requests.
  Delays too frequent requests.
* **configurable:**
  Exposes parameters of HTTP requests,
  logging,
  user input,
  API version,
  error handling,
  and so on.


Usage
-----

Authorisation
=============

.. code-block:: python

    >>> from pyvk import API
    >>> vk = API(api_id=<...>, username=<...>)
    Password: <...>

Password is requested only for the first time:
PyVK stores `API token`_ on disk and renews it automatically.
Secret code, mobile phone, and captcha
may also be requested during the initial authorisation.

.. _API token: https://new.vk.com/dev/access_token

One can also directly specify an API token obtained somewhere else:

.. code-block:: python

    >>> vk = API(token=<...>)

Method Calls
============

.. code-block:: python

    >>> vk.users.get(user_ids=['haroldpain'], fields=['home_town'])
    [{'last_name': 'Arató', 'home_town': 'Kőszeg', 'first_name': 'András', 'id': 329237321}]

    >>> albums = vk.photos.getAlbums(owner_id=329237321)
    >>> {a['title'] for a in albums['items']}
    {'Zuglói képek', 'In the arboretum of the Horticulture University in Budapest'}

See `list of methods`_ at VK developers section. Note that pythonic integers and lists can be used where the official API documentation specify numbers (including negative) and comma-separated lists.

.. _list of methods: https://new.vk.com/dev/methods


Credits
-------

Some ideas (such as first-class queryset-like methods) are inspired by `vk-requests`_.

.. _vk-requests: https://github.com/prawn-cake/vk-requests