# -----------------------------------------------------------------------------
# pyvk.helpers: reqn.py
#
# Implements helper to get `n' data items from API methods by a single function
# call without messing with `count' and `offset' parameters.
#
# Copyright (c) 2013-2016, Max Kuznetsov
# Licence: MIT
# -----------------------------------------------------------------------------


from itertools import chain, repeat, takewhile, accumulate, tee
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def reqn(partial_req, n=None, **api_method_args):

    method_name = partial_req.method_name()

    # Get two batch size iterators for offset calculation and for constructing
    # the (offset,size)-schedule.
    sizes_offset, sizes_shedule = tee(
        _get_batch_size_iter(method_name), 2
    )

    # Infinite generator of offsets:
    #   (0, steps_1, steps_1 + steps_2, ..., \sum{i=1}{m} steps_i)
    offsets_all = accumulate(chain([0], sizes_offset))

    # If `n' is set, cut offset sequence once it gets just below `n`.
    offsets = offsets_all if n is None \
        else takewhile(lambda x: x < n, offsets_all)

    # (offset,size)-schedule
    schedule = zip(offsets, sizes_shedule)

    if n is not None:
        # If `n' is set, change the last step to request exactly `n' items.
        # E.g. if the shedule ends with
        #   (... (off_m, step_m))
        # and (off_m + step_m) > n, the sequence becomes
        #   (... (off_m, n - off_m))
        schedule = ((off, size if (off+size) <= n else n - off)
                    for off, size in schedule)

    result = _init_result(method_name)

    for offset, size in schedule:
        logger.debug("Requesting batch: %s for offset=%d, count=%d"
                     % (method_name, offset, size))
        batch = partial_req(**dict(api_method_args, offset=offset, count=size))

        if _count_items(batch, method_name):
            _update_result(result, batch, method_name)
        else:
            break

    return result


def _get_batch_size_iter(method_name=None):
    """
    Returns iterator of maximum/optimal batch size for particular method_name.
    """
    if method_name == 'wall.get':
        return repeat(100)

    else:
        raise NotImplementedError('The API method'
                                  'does not support batch retrieval.')


def _count_items(data, method_name):
    return len(data['items'])


def _init_result(method_name):

    if method_name == 'wall.get':
        return {'count': 0, 'items': []}

    else:
        raise NotImplementedError('The API method'
                                  'does not support batch retrieval.')


def _update_result(result, data, method_name):
    result['count'] = data['count']
    result['items'].extend(data['items'])

    if method_name == 'wall.get':
        if 'groups' in data and 'profiles' in data:
            _merge_indexed_objects(result, data, 'profiles')
            _merge_indexed_objects(result, data, 'groups')

    else:
        raise NotImplementedError('The API method'
                                  'does not support batch retrieval.')

    return result


def _merge_indexed_objects(result, data, object_name, key='id'):
    objects = chain(result.get(object_name, []), data[object_name])
    # Filter duplicates by given key
    result[object_name] = list(
        {x[key]: x for x in objects}.values()
    )
