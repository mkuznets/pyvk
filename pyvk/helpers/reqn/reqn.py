# -*- coding: utf-8 -*-
"""
    pyvk.helpers.reqn.reqn
    ~~~~

    Implements helper to get `n' data item
    from API methods by a single function call
    without messing with `count' and `offset' parameters.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""


from itertools import chain, takewhile, accumulate, tee
import logging
import inspect
from . import results

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Index result classes by API method names
result_classes = {v.method_name: v
                  for k, v in inspect.getmembers(results, inspect.isclass)
                  if k.startswith('Result')}
logger.debug('Supported methods: %s' % list(result_classes.keys()))


def reqn(partial_req, n=None, **api_method_args):

    method_name = partial_req.method_name()
    result = result_classes[method_name](api_method_args)

    # Get two batch size iterators for offset calculation and for constructing
    # the (offset,size)-schedule.
    sizes_offset, sizes_shedule = tee(result.batch_size_iter, 2)

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
        schedule = [(off, size if (off+size) <= n else n - off)
                    for off, size in schedule]

        # Sanity test for total number of items.
        assert n == sum(s[1] for s in schedule)

    for offset, size in schedule:
        logger.debug("Requesting batch: %s for offset=%d, count=%d"
                     % (method_name, offset, size))
        data = partial_req(**dict(api_method_args, offset=offset, count=size))

        if result.is_new_items(data):
            result.update(data)
        else:
            break

    return result.result
