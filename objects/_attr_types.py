'''
The file describes custom datatypes for VK object fields declaration. Each type
is defined by a function testing whether its argument matches the datatype. The
function has to be named `test_<type_alias>`, had a single argument, and return
values interpretable as Boolean.
'''


## Common types.


def test_intp(x):
    '''
    Positive integers.
    '''
    return type(x) is int and x > 0


def test_intpz(x):
    '''
    Positive integers and zero.
    '''
    return type(x) is int and x >= 0


def test_flag(x):
    '''
    Binary flag: {0, 1}.
    '''
    return type(x) is int and 0 <= x <= 1


## Group


def test_int_0_1_2(x):
    '''
    Integers {0, 1, 2}.
    '''
    return type(x) is int and 0 <= x <= 2


def test_int_1_2_3(x):
    '''
    Integers {1, 2, 3}.
    '''
    return type(x) is int and 1 <= x <= 3


def test_group_deactivated(x):
    return x == 'deleted' or x == 'banned'


def test_group_type(x):
    return x == 'group' or x == 'page' or x == 'event'

## User


def test_user_deactivated(x):
    return x == 'deactivated' or x == 'banned'


def test_relation_int(x):
    return type(x) is int and 0 <= x <= 7


def test_int_1_2(x):
    return x == 1 or x == 2


def test_int_0_1_2_3(x):
    return type(x) is int and 0 <= x <= 3


def test_occupation_type(x):
    return x == 'work' or x == 'school' or x == 'unversity'


def test_political(x):
    return type(x) is int and 1 <= x <= 9


def test_people_main(x):
    return type(x) is int and 1 <= x <= 6


def test_life_main(x):
    return type(x) is int and 1 <= x <= 8


def test_view(x):
    return type(x) is int and 1 <= x <= 5

## Message


def test_push_settings(x):
    return x == 'sound' or x == 'disabled_until'


def test_action_str(x):
    return x in ('chat_photo_update', 'chat_photo_remove', 'chat_create',
                 'chat_title_update', 'chat_invite_user', 'chat_kick_user')


def test_int1(x):
    return x == 1


## Attachments
def test_attach_type(x):
    return x in ('photo', 'video', 'audio', 'doc', 'wall', 'wall_reply',
                 'sticker', 'posted_photo', 'graffiti', 'link', 'note', 'app',
                 'poll', 'page', 'album', 'photos_list')


## Privacy

def test_privacy_view(x):
    import re

    if type(x) is str:
        return x in ('all', 'friends', 'friends_of_friends',
                     'friends_of_friends_only', 'nobody', 'only_me') \
            or re.match('\-?list\d+', x)

    else:
        return type(x) is int
