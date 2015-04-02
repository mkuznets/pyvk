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
    return True if type(x) is int and x > 0 else False


def test_intpz(x):
    '''
    Positive integers and zero.
    '''
    return True if type(x) is int and x >= 0 else False


def test_flag(x):
    '''
    Binary flag: {0, 1}.
    '''
    return True if type(x) is int and 0 <= x <= 1 else False

## Group

def test_int_0_1_2(x):
    '''
    Integers {0, 1, 2}.
    '''
    return True if type(x) is int and 0 <= x <= 2 else False


def test_int_1_2_3(x):
    '''
    Integers {1, 2, 3}.
    '''
    return True if type(x) is int and 1 <= x <= 3 else False


def test_group_deactivated(x):
    return True if x == 'deleted' or x == 'banned' else False


def test_group_type(x):
    return True if x == 'group' or x == 'page' or x == 'event' else False
