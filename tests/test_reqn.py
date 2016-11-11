import os
import pytest
from pyvk import ClientAuth, p_wall, p_friends
from pyvk.utils import zip
from pyvk.helpers import reqn
from tests.utils import EnvInput

auth = ClientAuth(input=EnvInput, scope=p_wall|p_friends, disable_cache=True)
auth.auth()
api = auth.get_api()


def fetch(method, args, n, batch_size):
    rb = reqn(method, n=n, batch_size=batch_size, **args)
    rn = method(count=n, **args)
    return rb, rn


def fetch_and_compare(method, args, n, batch_size):

    rb, rn  = fetch(method, args, n, batch_size)

    if type(rb) is dict:
        assert set(rb.keys()) == set(rn.keys())

        for k in rb.keys():
            if type(rb[k]) is list:
                try:
                    ids_b = [e['id'] for e in rb[k]]
                    ids_n = [e['id'] for e in rn[k]]
                except TypeError:
                    ids_b = rb[k]
                    ids_n = rn[k]

                if k == 'items':
                    assert ids_b == ids_n
                else:
                    assert set(ids_b) == set(ids_n)

            else:
                assert rb[k] == rn[k]
    else:
        assert rb == rn


def test_reqn_exhaustive():
    method = api.friends.get
    args = dict(user_id=1)
    fetch_and_compare(method, args, None, batch_size=100)


def test_reqn_wall_get():
    method = api.wall.get
    args = dict(owner_id=-29534144, filter='owner', extended=1)
    fetch_and_compare(method, args, n=100, batch_size=10)

    args = dict(owner_id=-29534144, filter='owner')
    fetch_and_compare(method, args, n=100, batch_size=10)


def test_reqn_wall_getreposts():
    method = api.wall.getReposts
    args = dict(owner_id=-29534144, post_id=1347049)
    fetch_and_compare(method, args, n=40, batch_size=10)


def test_reqn_users_getsubscriptions():
    method = api.users.getSubscriptions

    with pytest.raises(ValueError):
        args = dict(user_id=1)
        fetch_and_compare(method, args, n=40, batch_size=10)

    args = dict(user_id=1, extended=1)
    fetch_and_compare(method, args, n=40, batch_size=10)


def test_reqn_friends_getonline():
    method = api.friends.getOnline

    n = 5
    # Online users are rather volatile, try several times.
    for attempt in range(n):
        try:
            args = dict(user_id=11651602, online_mobile=1)
            fetch_and_compare(method, args, n=50, batch_size=10)
            args = dict(user_id=11651602)
            fetch_and_compare(method, args, n=50, batch_size=10)

        except AssertionError:
            if attempt == n-1:
                raise
            else:
                continue

        break


def test_reqn_friends_getmutual():
    method = api.friends.getMutual

    args = dict(source_uid=1, target_uid=21)
    fetch_and_compare(method, args, n=35, batch_size=10)

    args = dict(source_uid=1, target_uids=[6,21])
    rb, rn = fetch(method, args, n=35, batch_size=10)

    for eb, en in zip(rb, rn):
        assert eb['common_friends'] == en['common_friends']


def test_reqn_storage_getkeys():
    method = api.storage.getKeys

    args = {'global': 1}
    fetch_and_compare(method, args, n=10, batch_size=1)
