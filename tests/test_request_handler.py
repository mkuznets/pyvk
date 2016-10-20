import mock
from pyvk.request import RequestHandler
from pyvk.config import RequestConfig
from collections import namedtuple

FakeAuth = namedtuple('Auth', 'token')
auth = FakeAuth(token='foo')
config = RequestConfig()


def test_request_handler_init():
    prefix = ['foo', 'bar']
    req_init = RequestHandler(prefix, auth, config)
    assert '.'.join(prefix) == req_init.method


def test_request_handler_append():
    prefix = ['foo', 'bar']
    suffix1 = 'buz'
    suffix2 = 'bam'
    req_init = RequestHandler(prefix, auth, config)

    req_final = getattr(req_init, suffix1)
    assert '.'.join(prefix + [suffix1]) == req_final.method

    # Multiple append
    req_final = getattr(req_final, suffix2)
    assert '.'.join(prefix + [suffix1, suffix2]) == req_final.method


def test_request_handler_call():

    with mock.patch('pyvk.request.Request') as r:
        args = {'c': 100, 'd': 1000}

        req = RequestHandler(['c0'], auth, config)
        req.c1.c2(**args)

        chained = mock.call('c0.c1.c2', args, auth, config).send()
        call_list = chained.call_list()

        print(r.mock_calls)
        print(call_list)

        assert r.mock_calls == call_list
