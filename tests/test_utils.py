import pytest
import mock
from pyvk import utils


def test_accumulate():
    assert [] == list(utils.accumulate([]))
    assert [42] == list(utils.accumulate([42]))
    assert [1, 3, 6, 10, 15, 21] == list(utils.accumulate([1, 2, 3, 4, 5, 6]))


def test_filter_dict():
    assert {} == utils.filter_dict({})
    assert {} == utils.filter_dict({'foo': None})
    assert {'bar': 42} == utils.filter_dict({'bar': 42, 'foo': None})


def test_process_args():
    assert {} == utils.process_args({})
    assert {'foo': 1} == utils.process_args({'foo': True})
    assert {'foo': 42} == utils.process_args({'foo': 42})
    assert {'foo': ''} == utils.process_args({'foo': []})
    assert {'foo': 'bar,42'} == utils.process_args({'foo': ['bar', 42]})


def test_input():

    mock_input = mock.Mock()
    mock_input.return_value = 'text'

    mock_getpass = mock.Mock()
    mock_getpass.return_value = 'qwerty'

    with mock.patch('pyvk.utils.input', new=mock_input):
        assert utils.Input.ask('username') == 'text'
        assert utils.Input.ask('app_id') == 'text'
        assert utils.Input.ask('secret_code') == 'text'
        assert utils.Input.ask('phone', msg='msg') == 'text'
        assert utils.Input.ask('captcha', img='img') == 'text'

        with pytest.raises(ValueError):
            utils.Input.ask('phone')

        with pytest.raises(ValueError):
            utils.Input.ask('captcha')

    with mock.patch('getpass.getpass', new=mock_getpass):
        assert utils.Input.ask('password') == 'qwerty'

    with pytest.raises(ValueError):
        utils.Input.ask('qqq')


class Global(utils.Config):
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


def test_len():
    config = Local()
    assert len(config) == 2


def test_repr():
    config = Local()
    assert eval(repr(config)) == config