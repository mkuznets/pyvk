.. PyVK documentation master file, created by
   sphinx-quickstart on Fri Oct  7 01:45:54 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyVK
===============

`VK`_ is one of the major Russian-speaking social networks.
PyVK is a Python library providing the simplest interface to `VK API`_.
It can be used for data retrieval and analysis, social media automation, and fun.

.. _VK: https://vk.com
.. _VK API: https://vk.com/dev/

.. code-block:: python

    >>> from pyvk import API
    >>> vk = API(api_id=<...>, username=<...>)
    Password: <...>
    >>> vk.users.get(user_ids=['haroldpain'], fields=['home_town'])
    [{'last_name': 'Arató', 'home_town': 'Kőszeg', 'first_name': 'András', 'id': 329237321}]
    >>> albums = vk.photos.getAlbums(owner_id=329237321)
    >>> {a['title'] for a in albums['items']}
    {'Zuglói képek', 'In the arboretum of the Horticulture University in Budapest'}

Apart from VK API methods we aim to simpify common routines such as batch data retrieval, photo uploading, event-driven workflow, and more. See :ref:`helpers` section for more details.

Features
--------

* **Authorisation:** PyVK automatically obtains, caches, and renews API access token. User credintials are requested only initially via an interactive session or a user-defined protocol. There is no need to store sensitive information in plain-text.
* **Method abstraction:** VK API methods are called as if they were pure pythonic. The responses are unwrapped and returned as dictionaries or lists.
* **Error handling:** PyVK detects and recovers from certain kinds of errors such as expired autorisation, temporal block, or captcha request.
* **Request bundling:** sometimes VK API cannot return all requested data items at once. In these cases PyVK can perform multiple requests and merge the results for you.

PyVK supports both Python 2 and 3.


User Guide
----------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   configuration
   helpers
