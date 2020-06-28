import os
import pytest
import mock
from pyvk.utils import DictNamedTuple


def test_len():
    d = DictNamedTuple(foo=42, bar='42')
    assert len(d) == 2


def test_missing():
    d = DictNamedTuple(foo=42, bar='42')

    with pytest.raises(KeyError):
        d['buz']
    with pytest.raises(AttributeError):
        d.buz


def test_eq():
    d1 = DictNamedTuple(foo=42, bar='42')
    d2 = DictNamedTuple(foo=42, bar='42')
    assert d1 == d2
    assert d1 != "foo"


def test_setattr():
    d1 = DictNamedTuple(foo=42, bar='42')
    with pytest.raises(AttributeError):
        d1.a = 100


def test_repr():
    d = DictNamedTuple(foo=42, bar='42')
    assert eval(repr(d)) == d


def test_source_mapping():

    d = DictNamedTuple({'a': 42}, a=43, b=45)

    assert list(d.keys()) == ['a', 'b']
    assert d.a == 43
    assert d['a'] == 43 and d['b'] == 45


def test_source_sequence():

    d = DictNamedTuple([('a', 42)], a=43, b=45)

    assert list(d.keys()) == ['a', 'b']
    assert d.a == 43
    assert d['a'] == 43 and d['b'] == 45


def test_source_error():

    with pytest.raises(TypeError):
        DictNamedTuple(100, a=43, b=45)
