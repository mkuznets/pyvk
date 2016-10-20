import pytest
from pyvk.config import Config


class Global(Config):
    foo = 1


class Local(Global):
    bar = 2


def test_inheritance():
    config = Local()
    assert config.foo == Global.foo
    assert config.bar == Local.bar


def test_init_nondefault():
    config = Local(foo=10, bar=100, buz=1000)
    assert config.foo == 10
    assert config.bar == 100
    with pytest.raises(AttributeError):
        config.buz


def test_change_protection():
    config = Local()
    with pytest.raises(AttributeError):
        config.bar = 100