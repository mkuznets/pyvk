import pytest

from pyvk import ClientAuth, p_basic, p_market, p_docs
from tests.utils import EnvInput


@pytest.fixture(scope='session')
def api():
    auth = ClientAuth(input=EnvInput, scope=p_basic | p_market | p_docs, disable_cache=True)
    auth.auth()
    return auth.api(max_attempts=100)
