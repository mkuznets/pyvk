import pytest
from pyvk.exceptions import PyVKError


def test_repr():
    exc = PyVKError('error', 42, bar=43)
    exc_repr = eval(repr(exc))
    assert exc_repr.args == exc.args
    assert exc_repr.kwargs == exc.kwargs
