import mock
from pyvk.api import PartialCall


def test_request_handler_init():
    prefix = ['foo', 'bar']
    call_init = PartialCall(prefix, None)
    assert '.'.join(prefix) == call_init.method


def test_append():
    prefix = ['foo', 'bar']
    suffix1 = 'buz'
    suffix2 = 'bam'
    call_init = PartialCall(prefix, None)

    call_final = getattr(call_init, suffix1)
    assert '.'.join(prefix + [suffix1]) == call_final.method

    # Multiple append
    call_final = getattr(call_final, suffix2)
    assert '.'.join(prefix + [suffix1, suffix2]) == call_final.method


def test_call():

    api = mock.Mock()
    args = {'c': 100, 'd': 1000}

    call = PartialCall(['c0'], api)
    call.c1.c2(**args)

    api_call = mock.call.call('c0.c1.c2', **args)

    assert len(api.mock_calls) == 1
    assert api.mock_calls[0] == api_call


def test_repr():
    call = PartialCall(['foo', 'bar'], None)
    assert call.method in repr(call)