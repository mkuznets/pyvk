# VK API for Python

[![Tests](https://github.com/mkuznets/pyvk/actions/workflows/main.yml/badge.svg)](https://github.com/mkuznets/pyvk/actions/workflows/main.yml)
[![image](https://coveralls.io/repos/github/mkuznets/pyvk/badge.svg?branch=master)](https://coveralls.io/github/mkuznets/pyvk?branch=master)
[![image](https://img.shields.io/pypi/v/pyvk.svg?style=flat)](https://pypi.python.org/pypi/pyvk)

[VK](https://vk.com) is one of the major Russian-speaking social
networks. **PyVK** is a no-nonsence boilerplate-free [VK
API](https://vk.com/dev/) library for Python. It can be used in server
or client applications, scripts, or interactively for data retrieval and
analysis, social media integration, automation, and fun.

## Features

- **Authorisation:** PyVK assists both client- and server-side
  authorisation. It ensures that your password is not stored anywhere in
  plain-text. It also supports 2FA and captcha/mobile phone login
  confirmation.
- **Error handling:** PyVK wraps API errors into exceptions and can
  recover from certain kinds of those, such as expired autorisation,
  temporal ban, or captcha request.
- **Pagination:** PyVK can join paginated API responses into a single
  result.
- **Media uploading:** PyVK wraps it into a single method call and makes
  it easy to use those files as attachments to posts and messages.
- **Python 2 and 3 :** PyVK is tested for CPython 2.7 and 3.5-3.8

## Examples

``` python
>>> from pyvk import ClientAuth, p_docs, p_offline

>>> # Authorisation without tokens and stored passwords
>>> auth = ClientAuth(app_id=<...>, username=<...>, scope=p_docs | p_offline)
>>> auth.auth()
Password: <...>

>>> api = auth.api(version='5.21', lang='en')

>>> # Call API methods as if they were pythonic
>>> api.users.get(user_ids=[210700286], fields=['bdate'])
[{'id': 210700286,
  'first_name': 'Lindsey',
  'last_name': 'Stirling',
  'bdate': '21.9.1986'}]

>>> # Fetch all items from paginated API responses with a single call
>>> from pyvk.helpers import reqn
>>> reqn(api.users.getFollowers, n=1000, user_id=53083705)
{'count': 2255643,
 'items': [404278316,
           372620717,
           405001689,
           ...]}

>>> # Easy file uploading
>>> from pyvk.helpers.uploaders import WallPhotoUploader
>>> up = WallPhotoUploader(api)
>>> with open('cat.jpg', 'rb') as f:
>>>    attach = up.upload(f, attach=True)
>>>    api.wall.post(attachments=attach)
```

## Installation

Stable versions can be installed using
[pip](https://pypi.python.org/pypi/pip):

``` 
pip install pyvk
```

For development version:

``` 
pip install git+https://github.com/mkuznets/pyvk.git@master
```
