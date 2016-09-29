# -*- coding: utf-8 -*-
"""
    pyvk.helpers.reqn.results
    ~~~~

    Defines classes for results of particular VK API methods calls.
    They mainly implement merging multiple results into a single one.

    :copyright: (c) 2013-2016 by Max Kuznetsov.
    :license: MIT, see LICENSE for more details.
"""


from itertools import chain, repeat


class _Result:
    method_name = None
    result = None
    batch_size_iter = None

    def _merge_indexed_objects(self, data, object_name, key='id'):
        objects = chain(self.result[object_name], data[object_name])

        # Filter duplicates by given key
        self.result[object_name] = list(
            {x[key]: x for x in objects}.values()
        )


class ResultWallGet(_Result):
    method_name = 'wall.get'

    def __init__(self, args):
        self.result = {'count': 0, 'items': []}
        self.batch_size_iter = repeat(100)
        self.extended = False

        if args.get('extended', False):
            self.result.update({'profiles': [], 'groups': []})
            self.extended = True

    def count_new_items(self, data):
        return len(data['items'])

    def update(self, data):
        self.result['count'] = data['count']
        self.result['items'].extend(data['items'])

        if self.extended:
            self._merge_indexed_objects(data, 'profiles')
            self._merge_indexed_objects(data, 'groups')


class ResultUsersSearch(_Result):
    method_name = 'users.search'

    def __init__(self, args):
        self.result = {'count': 0, 'items': []}
        self.batch_size_iter = repeat(1000)

    def count_new_items(self, data):
        return len(data['items'])

    def update(self, data):
        self.result['count'] = data['count']
        self.result['items'].extend(data['items'])
