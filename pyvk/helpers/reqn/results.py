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

    def count_new_items(self, data):
        return len(data['items'])


class ResultItemList(_Result):
    _batch_size = 1000

    def __init__(self, args):
        self.result = {'count': 0, 'items': []}
        self.batch_size_iter = repeat(self._batch_size)

    def update(self, data):
        self.result['count'] = data['count']
        self.result['items'].extend(data['items'])


class ResultWallGet(_Result):
    method_name = 'wall.get'

    def __init__(self, args):
        self.result = {'count': 0, 'items': []}
        self.batch_size_iter = repeat(100)
        self.extended = False

        if args.get('extended', False):
            self.result.update({'profiles': [], 'groups': []})
            self.extended = True

    def update(self, data):
        self.result['count'] = data['count']
        self.result['items'].extend(data['items'])

        if self.extended:
            self._merge_indexed_objects(data, 'profiles')
            self._merge_indexed_objects(data, 'groups')


class ResultWallGetReposts(_Result):
    method_name = 'wall.getReposts'

    def __init__(self, args):
        self.result = {'items': [], 'profiles': [], 'groups': []}
        self.batch_size_iter = repeat(1000)

    def update(self, data):
        self.result['items'].extend(data['items'])
        self._merge_indexed_objects(data, 'profiles')
        self._merge_indexed_objects(data, 'groups')


class ResultWallSearch(ResultWallGet):
    method_name = 'wall.search'


class ResultUsersSearch(ResultItemList):
    method_name = 'users.search'


class ResultUsersGetFollowers(ResultItemList):
    method_name = 'users.getFollowers'


class ResultUsersGetSubscriptions(ResultItemList):
    method_name = 'users.getSubscriptions'
    _batch_size = 200

    def __init__(self, args):
        if 'extended' not in args:
            raise ValueError('users.getSubscriptions: '
                             'batch request requires extended=1')
        super().__init__(args)


class ResultFriendsGet(ResultItemList):
    method_name = 'friends.get'
    _batch_size = 5000


class ResultGroupsGet(ResultItemList):
    method_name = 'groups.get'


class ResultGroupsGetMembers(ResultItemList):
    method_name = 'groups.getMembers'


class ResultPhotosGet(ResultItemList):
    method_name = 'photos.get'


class ResultPhotosSearch(ResultItemList):
    method_name = 'photos.search'


class ResultPhotosGetAlbums(ResultItemList):
    method_name = 'photos.getAlbums'
    # NOTE: batch size is not mentioned in documentation, assume default


class ResultPhotosGetUserPhotos(ResultItemList):
    method_name = 'photos.getUserPhotos'


class ResultPhotosGetAllComments(ResultItemList):
    method_name = 'photos.getAllComments'
    _batch_size = 100


class ResultPhotosGetNewTags(ResultItemList):
    method_name = 'photos.getNewTags'
    _batch_size = 100


class ResultFriendsGetOnline(_Result):
    method_name = 'friends.getOnline'

    def __init__(self, args):
        self.online_mobile = bool(args.get('online_mobile', False))

        self.result = {'online': [], 'online_mobile': []} \
            if self.online_mobile else []

        self.batch_size_iter = repeat(100000)  # the size is not limited

    def update(self, data):
        if self.online_mobile:
            self.result['online'].extend(data['online'])
            self.result['online_mobile'].extend(data['online_mobile'])
        else:
            assert isinstance(data, list)
            self.result.extend(data)

    def count_new_items(self, data):
        if self.online_mobile:
            return len(data['online']) + len(data['online_mobile'])
        else:
            assert isinstance(data, list)
            return len(data)



# TODO

# Static schedule:
#
# + users.search
# + users.getSubscriptions
# + users.getFollowers
# + wall.get
# + wall.search
# + wall.getReposts
# + photos.getAlbums
# + photos.get
# + photos.search
# + photos.getUserPhotos
# + photos.getAllComments
# + photos.getNewTags
# + friends.get
# + friends.getOnline
# friends.getMutual
# friends.getRequests
# friends.getSuggestions
# friends.search
# widgets.getComments
# widgets.getPages
# storage.getKeys
# audio.get
# audio.search
# audio.getAlbums
# audio.getRecommendations
# audio.getPopular
# + groups.get
# + groups.getMembers
# groups.search
# groups.getInvites
# groups.getInvitedUsers
# groups.getBanned
# groups.getRequests
# board.getTopics
# video.get
# video.search
# video.getUserVideos
# video.getAlbums
# video.getNewTags
# notes.get
# notes.getComments
# places.search
# places.getCheckins
# account.getActiveOffers
# account.getBanned
# messages.getDialogs
# messages.search
# messages.getHistory
# messages.deleteDialog
# newsfeed.get
# newsfeed.getRecommended
# newsfeed.getMentions
# newsfeed.search
# newsfeed.getSuggestedSources
# likes.getList
# polls.getVoters
# docs.get
# docs.search
# fave.getUsers
# fave.getPhotos
# fave.getPosts
# fave.getVideos
# fave.getLinks
# fave.getMarketItems
# notifications.get
# apps.getCatalog
# apps.getFriendsList
# database.getCountries
# database.getRegions
# database.getCities
# database.getUniversities
# database.getSchools
# database.getFaculties
# database.getChairs
# gifts.get
# market.get
# market.search
# market.getAlbums
# market.getComments
# market.getCategories

# Dynamic shecule:
#
# wall.getComments
# photos.getAll
# photos.getComments
# board.getComments
# video.getComments
# messages.getDialogs
# messages.get
