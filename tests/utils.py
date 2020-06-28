from pyvk.utils import Input
import json
import os


class EnvInput(Input):
    @staticmethod
    def ask(field, **kwargs):

        if field == 'username':
            return os.environ['API_USER']

        elif field == 'app_id':
            return os.environ['API_ID']

        elif field == 'password':
            return os.environ['API_PASS']

        elif field == 'phone':
            return os.environ['API_USER'][2:-2]

        else:
            raise ValueError('Unknown field')


class Session(object):
    def __init__(self, handler, **kwargs):
        self.handler = handler
        self.cookies = {}
        self.kwargs = kwargs
        super(Session, self).__init__()

    def get(self, url, *args, **kwargs):
        kwargs = dict(kwargs)
        kwargs.update(self.kwargs)
        return self.handler('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        kwargs = dict(kwargs)
        kwargs.update(self.kwargs)
        return self.handler('POST', url, *args, **kwargs)


def selector(session):
    def _callable(*args, **kwargs):
        return session

    return _callable


class Response(object):
    def __init__(self, url, content):
        self.url = url
        self.content = content

    def json(self):
        return json.loads(self.text)

    @property
    def text(self):
        return self.content.decode()


class Fake(Input):
    @staticmethod
    def ask(field, **kwargs):
        if field == 'secret_code':
            return 'fooooo'
        elif field == 'phone':
            return '2323442'
        elif field == 'password':
            return 'qwerty'
