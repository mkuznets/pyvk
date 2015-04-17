class PlainObject(object):

    def __init__(self, **kwargs):

        for attr in ('__attrs__', '__attrs_required__'):
            if not hasattr(self, attr):
                raise NotImplementedError(attr + ' attribute is required.')

        for attr in self.__attrs__:
            value = kwargs.get(attr, None)

            if value is None and attr in self.__attrs_required__:
                raise ValueError('%s.%s: value is required.' %
                                 (self.__class__.__name__, attr))

            setattr(self, '_%s' % attr, value)


class VKObject(PlainObject):

    def _fetch_field(self, attr):
        # Default behaviour: return the underlying attribute value.
        return getattr(self, '_%s' % attr, None)


class Post(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'from_id', 'date', 'text',
        'reply_owner_id', 'reply_post_id', 'friends_only', 'comments', 'likes',
        'reposts', 'post_type', 'post_source', 'attachments', 'geo',
        'signer_id', 'copy_history', 'can_pin', 'is_pinned')
        self.__attrs_required__ = set(['id', 'owner_id', 'date', 'comments'])

        super(Post, self).__init__(**kwargs)

    @property
    def id(self):
        if self._id is None:
            self._id = self._fetch_field('id')
        return self._id

    @id.setter
    def id(self, x):
        if test_intp(x):
            self._id = x
        else:
            raise TypeError("Post.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if type(x) is int:
            self._owner_id = x
        else:
            raise TypeError("Post.owner_id: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def from_id(self):
        if self._from_id is None:
            self._from_id = self._fetch_field('from_id')
        return self._from_id

    @from_id.setter
    def from_id(self, x):
        if type(x) is int:
            self._from_id = x
        else:
            raise TypeError("Post.from_id: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def date(self):
        if self._date is None:
            self._date = self._fetch_field('date')
        return self._date

    @date.setter
    def date(self, x):
        if test_intp(x):
            self._date = x
        else:
            raise TypeError("Post.date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def text(self):
        if self._text is None:
            self._text = self._fetch_field('text')
        return self._text

    @text.setter
    def text(self, x):
        if type(x) is str:
            self._text = x
        else:
            raise TypeError("Post.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def reply_owner_id(self):
        if self._reply_owner_id is None:
            self._reply_owner_id = self._fetch_field('reply_owner_id')
        return self._reply_owner_id

    @reply_owner_id.setter
    def reply_owner_id(self, x):
        if type(x) is int:
            self._reply_owner_id = x
        else:
            raise TypeError("Post.reply_owner_id: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def reply_post_id(self):
        if self._reply_post_id is None:
            self._reply_post_id = self._fetch_field('reply_post_id')
        return self._reply_post_id

    @reply_post_id.setter
    def reply_post_id(self, x):
        if test_intp(x):
            self._reply_post_id = x
        else:
            raise TypeError("Post.reply_post_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def friends_only(self):
        if self._friends_only is None:
            self._friends_only = self._fetch_field('friends_only')
        return self._friends_only

    @friends_only.setter
    def friends_only(self, x):
        if test_flag(x):
            self._friends_only = x
        else:
            raise TypeError("Post.friends_only: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def comments(self):
        if self._comments is None:
            self._comments = self._fetch_field('comments')
        return self._comments

    @comments.setter
    def comments(self, x):
        if type(x) is CommentsInfo:
            self._comments = x
        else:
            raise TypeError("Post.comments: cannot set attribute with value"
                            " of type `%s', `CommentsInfo' expected" % x.__class__.__name__)

    @property
    def likes(self):
        if self._likes is None:
            self._likes = self._fetch_field('likes')
        return self._likes

    @likes.setter
    def likes(self, x):
        if type(x) is LikesInfo:
            self._likes = x
        else:
            raise TypeError("Post.likes: cannot set attribute with value"
                            " of type `%s', `LikesInfo' expected" % x.__class__.__name__)

    @property
    def reposts(self):
        if self._reposts is None:
            self._reposts = self._fetch_field('reposts')
        return self._reposts

    @reposts.setter
    def reposts(self, x):
        if type(x) is RepostsInfo:
            self._reposts = x
        else:
            raise TypeError("Post.reposts: cannot set attribute with value"
                            " of type `%s', `RepostsInfo' expected" % x.__class__.__name__)

    @property
    def post_type(self):
        if self._post_type is None:
            self._post_type = self._fetch_field('post_type')
        return self._post_type

    @post_type.setter
    def post_type(self, x):
        if type(x) is str:
            self._post_type = x
        else:
            raise TypeError("Post.post_type: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def post_source(self):
        if self._post_source is None:
            self._post_source = self._fetch_field('post_source')
        return self._post_source

    @post_source.setter
    def post_source(self, x):
        if type(x) is Source:
            self._post_source = x
        else:
            raise TypeError("Post.post_source: cannot set attribute with value"
                            " of type `%s', `Source' expected" % x.__class__.__name__)

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = self._fetch_field('attachments')
        return self._attachments

    @attachments.setter
    def attachments(self, x):
        if type(x) is Attachment:
            self._attachments = x
        else:
            raise TypeError("Post.attachments: cannot set attribute with value"
                            " of type `%s', `Attachment' expected" % x.__class__.__name__)

    @property
    def geo(self):
        if self._geo is None:
            self._geo = self._fetch_field('geo')
        return self._geo

    @geo.setter
    def geo(self, x):
        if type(x) is Geo:
            self._geo = x
        else:
            raise TypeError("Post.geo: cannot set attribute with value"
                            " of type `%s', `Geo' expected" % x.__class__.__name__)

    @property
    def signer_id(self):
        if self._signer_id is None:
            self._signer_id = self._fetch_field('signer_id')
        return self._signer_id

    @signer_id.setter
    def signer_id(self, x):
        if test_intp(x):
            self._signer_id = x
        else:
            raise TypeError("Post.signer_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def copy_history(self):
        if self._copy_history is None:
            self._copy_history = self._fetch_field('copy_history')
        return self._copy_history

    @copy_history.setter
    def copy_history(self, x):
        if type(x) is Post:
            self._copy_history = x
        else:
            raise TypeError("Post.copy_history: cannot set attribute with value"
                            " of type `%s', `Post' expected" % x.__class__.__name__)

    @property
    def can_pin(self):
        if self._can_pin is None:
            self._can_pin = self._fetch_field('can_pin')
        return self._can_pin

    @can_pin.setter
    def can_pin(self, x):
        if test_flag(x):
            self._can_pin = x
        else:
            raise TypeError("Post.can_pin: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def is_pinned(self):
        if self._is_pinned is None:
            self._is_pinned = self._fetch_field('is_pinned')
        return self._is_pinned

    @is_pinned.setter
    def is_pinned(self, x):
        if test_flag(x):
            self._is_pinned = x
        else:
            raise TypeError("Post.is_pinned: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


class CommentsInfo(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('count', 'can_post')
        self.__attrs_required__ = set(['count', 'can_post'])

        super(CommentsInfo, self).__init__(**kwargs)

    @property
    def count(self):
        if self._count is None:
            self._count = self._fetch_field('count')
        return self._count

    @count.setter
    def count(self, x):
        if test_intp(x):
            self._count = x
        else:
            raise TypeError("CommentsInfo.count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def can_post(self):
        if self._can_post is None:
            self._can_post = self._fetch_field('can_post')
        return self._can_post

    @can_post.setter
    def can_post(self, x):
        if test_flag(x):
            self._can_post = x
        else:
            raise TypeError("CommentsInfo.can_post: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


class LikesInfo(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('count', 'user_likes', 'can_like', 'can_publish')
        self.__attrs_required__ = set(['count', 'user_likes', 'can_like', 'can_publish'])

        super(LikesInfo, self).__init__(**kwargs)

    @property
    def count(self):
        if self._count is None:
            self._count = self._fetch_field('count')
        return self._count

    @count.setter
    def count(self, x):
        if test_intp(x):
            self._count = x
        else:
            raise TypeError("LikesInfo.count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_likes(self):
        if self._user_likes is None:
            self._user_likes = self._fetch_field('user_likes')
        return self._user_likes

    @user_likes.setter
    def user_likes(self, x):
        if test_flag(x):
            self._user_likes = x
        else:
            raise TypeError("LikesInfo.user_likes: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_like(self):
        if self._can_like is None:
            self._can_like = self._fetch_field('can_like')
        return self._can_like

    @can_like.setter
    def can_like(self, x):
        if test_flag(x):
            self._can_like = x
        else:
            raise TypeError("LikesInfo.can_like: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_publish(self):
        if self._can_publish is None:
            self._can_publish = self._fetch_field('can_publish')
        return self._can_publish

    @can_publish.setter
    def can_publish(self, x):
        if test_flag(x):
            self._can_publish = x
        else:
            raise TypeError("LikesInfo.can_publish: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


class RepostsInfo(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('count', 'user_reposted')
        self.__attrs_required__ = set(['count', 'user_reposted'])

        super(RepostsInfo, self).__init__(**kwargs)

    @property
    def count(self):
        if self._count is None:
            self._count = self._fetch_field('count')
        return self._count

    @count.setter
    def count(self, x):
        if test_intp(x):
            self._count = x
        else:
            raise TypeError("RepostsInfo.count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_reposted(self):
        if self._user_reposted is None:
            self._user_reposted = self._fetch_field('user_reposted')
        return self._user_reposted

    @user_reposted.setter
    def user_reposted(self, x):
        if test_flag(x):
            self._user_reposted = x
        else:
            raise TypeError("RepostsInfo.user_reposted: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


class Source(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('type', 'platform', 'data', 'url')
        self.__attrs_required__ = set(['type', 'platform', 'url'])

        super(Source, self).__init__(**kwargs)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if type(x) is src_type:
            self._type = x
        else:
            raise TypeError("Source.type: cannot set attribute with value"
                            " of type `%s', `src_type' expected" % x.__class__.__name__)

    @property
    def platform(self):
        if self._platform is None:
            self._platform = self._fetch_field('platform')
        return self._platform

    @platform.setter
    def platform(self, x):
        if type(x) is src_platform:
            self._platform = x
        else:
            raise TypeError("Source.platform: cannot set attribute with value"
                            " of type `%s', `src_platform' expected" % x.__class__.__name__)

    @property
    def data(self):
        if self._data is None:
            self._data = self._fetch_field('data')
        return self._data

    @data.setter
    def data(self, x):
        if type(x) is SrcData:
            self._data = x
        else:
            raise TypeError("Source.data: cannot set attribute with value"
                            " of type `%s', `SrcData' expected" % x.__class__.__name__)

    @property
    def url(self):
        if self._url is None:
            self._url = self._fetch_field('url')
        return self._url

    @url.setter
    def url(self, x):
        if type(x) is str:
            self._url = x
        else:
            raise TypeError("Source.url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Group(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'name', 'screen_name', 'is_closed',
        'deactivated', 'is_admin', 'admin_level', 'is_member', 'type',
        'photo_50', 'photo_100', 'photo_200', 'ban_info', 'city', 'country',
        'place', 'description', 'wiki_page', 'members_count', 'counters',
        'start_date', 'finish_date', 'can_post', 'can_see_all_posts',
        'can_upload_doc', 'can_upload_video', 'can_create_topic', 'activity',
        'status', 'contacts', 'links', 'fixed_post', 'verified', 'site',
        'main_album_id', 'is_favorite')
        self.__attrs_required__ = set()

        super(Group, self).__init__(**kwargs)

    @property
    def id(self):
        if self._id is None:
            self._id = self._fetch_field('id')
        return self._id

    @id.setter
    def id(self, x):
        if test_intp(x):
            self._id = x
        else:
            raise TypeError("Group.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def name(self):
        if self._name is None:
            self._name = self._fetch_field('name')
        return self._name

    @name.setter
    def name(self, x):
        if type(x) is str:
            self._name = x
        else:
            raise TypeError("Group.name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def screen_name(self):
        if self._screen_name is None:
            self._screen_name = self._fetch_field('screen_name')
        return self._screen_name

    @screen_name.setter
    def screen_name(self, x):
        if type(x) is str:
            self._screen_name = x
        else:
            raise TypeError("Group.screen_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def is_closed(self):
        if self._is_closed is None:
            self._is_closed = self._fetch_field('is_closed')
        return self._is_closed

    @is_closed.setter
    def is_closed(self, x):
        if test_int_0_1_2(x):
            self._is_closed = x
        else:
            raise TypeError("Group.is_closed: cannot set attribute with value"
                            " of type `%s', `int_0_1_2' expected" % x.__class__.__name__)

    @property
    def deactivated(self):
        if self._deactivated is None:
            self._deactivated = self._fetch_field('deactivated')
        return self._deactivated

    @deactivated.setter
    def deactivated(self, x):
        if test_group_deactivated(x):
            self._deactivated = x
        else:
            raise TypeError("Group.deactivated: cannot set attribute with value"
                            " of type `%s', `group_deactivated' expected" % x.__class__.__name__)

    @property
    def is_admin(self):
        if self._is_admin is None:
            self._is_admin = self._fetch_field('is_admin')
        return self._is_admin

    @is_admin.setter
    def is_admin(self, x):
        if test_flag(x):
            self._is_admin = x
        else:
            raise TypeError("Group.is_admin: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def admin_level(self):
        if self._admin_level is None:
            self._admin_level = self._fetch_field('admin_level')
        return self._admin_level

    @admin_level.setter
    def admin_level(self, x):
        if test_int_1_2_3(x):
            self._admin_level = x
        else:
            raise TypeError("Group.admin_level: cannot set attribute with value"
                            " of type `%s', `int_1_2_3' expected" % x.__class__.__name__)

    @property
    def is_member(self):
        if self._is_member is None:
            self._is_member = self._fetch_field('is_member')
        return self._is_member

    @is_member.setter
    def is_member(self, x):
        if test_flag(x):
            self._is_member = x
        else:
            raise TypeError("Group.is_member: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if test_group_type(x):
            self._type = x
        else:
            raise TypeError("Group.type: cannot set attribute with value"
                            " of type `%s', `group_type' expected" % x.__class__.__name__)

    @property
    def photo_50(self):
        if self._photo_50 is None:
            self._photo_50 = self._fetch_field('photo_50')
        return self._photo_50

    @photo_50.setter
    def photo_50(self, x):
        if type(x) is str:
            self._photo_50 = x
        else:
            raise TypeError("Group.photo_50: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_100(self):
        if self._photo_100 is None:
            self._photo_100 = self._fetch_field('photo_100')
        return self._photo_100

    @photo_100.setter
    def photo_100(self, x):
        if type(x) is str:
            self._photo_100 = x
        else:
            raise TypeError("Group.photo_100: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_200(self):
        if self._photo_200 is None:
            self._photo_200 = self._fetch_field('photo_200')
        return self._photo_200

    @photo_200.setter
    def photo_200(self, x):
        if type(x) is str:
            self._photo_200 = x
        else:
            raise TypeError("Group.photo_200: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def ban_info(self):
        if self._ban_info is None:
            self._ban_info = self._fetch_field('ban_info')
        return self._ban_info

    @ban_info.setter
    def ban_info(self, x):
        if type(x) is BanInfo:
            self._ban_info = x
        else:
            raise TypeError("Group.ban_info: cannot set attribute with value"
                            " of type `%s', `BanInfo' expected" % x.__class__.__name__)

    @property
    def city(self):
        if self._city is None:
            self._city = self._fetch_field('city')
        return self._city

    @city.setter
    def city(self, x):
        if test_intpz(x):
            self._city = x
        else:
            raise TypeError("Group.city: cannot set attribute with value"
                            " of type `%s', `intpz' expected" % x.__class__.__name__)

    @property
    def country(self):
        if self._country is None:
            self._country = self._fetch_field('country')
        return self._country

    @country.setter
    def country(self, x):
        if test_intpz(x):
            self._country = x
        else:
            raise TypeError("Group.country: cannot set attribute with value"
                            " of type `%s', `intpz' expected" % x.__class__.__name__)

    @property
    def place(self):
        if self._place is None:
            self._place = self._fetch_field('place')
        return self._place

    @place.setter
    def place(self, x):
        if type(x) is GroupPlace:
            self._place = x
        else:
            raise TypeError("Group.place: cannot set attribute with value"
                            " of type `%s', `GroupPlace' expected" % x.__class__.__name__)

    @property
    def description(self):
        if self._description is None:
            self._description = self._fetch_field('description')
        return self._description

    @description.setter
    def description(self, x):
        if type(x) is str:
            self._description = x
        else:
            raise TypeError("Group.description: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def wiki_page(self):
        if self._wiki_page is None:
            self._wiki_page = self._fetch_field('wiki_page')
        return self._wiki_page

    @wiki_page.setter
    def wiki_page(self, x):
        if type(x) is str:
            self._wiki_page = x
        else:
            raise TypeError("Group.wiki_page: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def members_count(self):
        if self._members_count is None:
            self._members_count = self._fetch_field('members_count')
        return self._members_count

    @members_count.setter
    def members_count(self, x):
        if test_intpz(x):
            self._members_count = x
        else:
            raise TypeError("Group.members_count: cannot set attribute with value"
                            " of type `%s', `intpz' expected" % x.__class__.__name__)

    @property
    def counters(self):
        if self._counters is None:
            self._counters = self._fetch_field('counters')
        return self._counters

    @counters.setter
    def counters(self, x):
        if test_intpz(x):
            self._counters = x
        else:
            raise TypeError("Group.counters: cannot set attribute with value"
                            " of type `%s', `intpz' expected" % x.__class__.__name__)

    @property
    def start_date(self):
        if self._start_date is None:
            self._start_date = self._fetch_field('start_date')
        return self._start_date

    @start_date.setter
    def start_date(self, x):
        if test_intp(x):
            self._start_date = x
        else:
            raise TypeError("Group.start_date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def finish_date(self):
        if self._finish_date is None:
            self._finish_date = self._fetch_field('finish_date')
        return self._finish_date

    @finish_date.setter
    def finish_date(self, x):
        if test_intp(x):
            self._finish_date = x
        else:
            raise TypeError("Group.finish_date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def can_post(self):
        if self._can_post is None:
            self._can_post = self._fetch_field('can_post')
        return self._can_post

    @can_post.setter
    def can_post(self, x):
        if test_flag(x):
            self._can_post = x
        else:
            raise TypeError("Group.can_post: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_see_all_posts(self):
        if self._can_see_all_posts is None:
            self._can_see_all_posts = self._fetch_field('can_see_all_posts')
        return self._can_see_all_posts

    @can_see_all_posts.setter
    def can_see_all_posts(self, x):
        if test_flag(x):
            self._can_see_all_posts = x
        else:
            raise TypeError("Group.can_see_all_posts: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_upload_doc(self):
        if self._can_upload_doc is None:
            self._can_upload_doc = self._fetch_field('can_upload_doc')
        return self._can_upload_doc

    @can_upload_doc.setter
    def can_upload_doc(self, x):
        if test_flag(x):
            self._can_upload_doc = x
        else:
            raise TypeError("Group.can_upload_doc: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_upload_video(self):
        if self._can_upload_video is None:
            self._can_upload_video = self._fetch_field('can_upload_video')
        return self._can_upload_video

    @can_upload_video.setter
    def can_upload_video(self, x):
        if test_flag(x):
            self._can_upload_video = x
        else:
            raise TypeError("Group.can_upload_video: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_create_topic(self):
        if self._can_create_topic is None:
            self._can_create_topic = self._fetch_field('can_create_topic')
        return self._can_create_topic

    @can_create_topic.setter
    def can_create_topic(self, x):
        if test_flag(x):
            self._can_create_topic = x
        else:
            raise TypeError("Group.can_create_topic: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def activity(self):
        if self._activity is None:
            self._activity = self._fetch_field('activity')
        return self._activity

    @activity.setter
    def activity(self, x):
        if type(x) is str:
            self._activity = x
        else:
            raise TypeError("Group.activity: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def status(self):
        if self._status is None:
            self._status = self._fetch_field('status')
        return self._status

    @status.setter
    def status(self, x):
        if type(x) is str:
            self._status = x
        else:
            raise TypeError("Group.status: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def contacts(self):
        if self._contacts is None:
            self._contacts = self._fetch_field('contacts')
        return self._contacts

    @contacts.setter
    def contacts(self, x):
        if type(x) is str:
            self._contacts = x
        else:
            raise TypeError("Group.contacts: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def links(self):
        if self._links is None:
            self._links = self._fetch_field('links')
        return self._links

    @links.setter
    def links(self, x):
        if type(x) is str:
            self._links = x
        else:
            raise TypeError("Group.links: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def fixed_post(self):
        if self._fixed_post is None:
            self._fixed_post = self._fetch_field('fixed_post')
        return self._fixed_post

    @fixed_post.setter
    def fixed_post(self, x):
        if test_intp(x):
            self._fixed_post = x
        else:
            raise TypeError("Group.fixed_post: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def verified(self):
        if self._verified is None:
            self._verified = self._fetch_field('verified')
        return self._verified

    @verified.setter
    def verified(self, x):
        if test_flag(x):
            self._verified = x
        else:
            raise TypeError("Group.verified: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def site(self):
        if self._site is None:
            self._site = self._fetch_field('site')
        return self._site

    @site.setter
    def site(self, x):
        if type(x) is str:
            self._site = x
        else:
            raise TypeError("Group.site: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def main_album_id(self):
        if self._main_album_id is None:
            self._main_album_id = self._fetch_field('main_album_id')
        return self._main_album_id

    @main_album_id.setter
    def main_album_id(self, x):
        if test_intp(x):
            self._main_album_id = x
        else:
            raise TypeError("Group.main_album_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def is_favorite(self):
        if self._is_favorite is None:
            self._is_favorite = self._fetch_field('is_favorite')
        return self._is_favorite

    @is_favorite.setter
    def is_favorite(self, x):
        if test_flag(x):
            self._is_favorite = x
        else:
            raise TypeError("Group.is_favorite: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


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

