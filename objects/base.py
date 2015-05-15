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


class User(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'first_name', 'last_name', 'deactivated',
        'hidden', 'photo_id', 'verified', 'blacklisted', 'sex', 'bdate',
        'city', 'country', 'home_town', 'photo_50', 'photo_100',
        'photo_200_orig', 'photo_200', 'photo_400_orig', 'photo_max',
        'photo_max_orig', 'online', 'lists', 'domain', 'has_mobile',
        'contacts', 'site', 'education', 'universities', 'schools', 'status',
        'last_seen', 'followers_count', 'common_count', 'counters',
        'occupation', 'nickname', 'relatives', 'relation', 'personal',
        'connections', 'twitter', 'livejornal', 'instagram', 'skype',
        'facebook', 'exports', 'wall_comments', 'activities', 'interests',
        'music', 'movies', 'tv', 'books', 'games', 'about', 'quotes',
        'can_post', 'can_see_all_posts', 'can_see_audio',
        'can_write_private_message', 'can_send_friend_request', 'is_favorite',
        'timezone', 'screen_name', 'maiden_name', 'crop_photo', 'is_friend',
        'friend_status')
        self.__attrs_required__ = set(['id', 'first_name', 'last_name', 'sex'])

        super(User, self).__init__(**kwargs)

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
            raise TypeError("User.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def first_name(self):
        if self._first_name is None:
            self._first_name = self._fetch_field('first_name')
        return self._first_name

    @first_name.setter
    def first_name(self, x):
        if type(x) is str:
            self._first_name = x
        else:
            raise TypeError("User.first_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def last_name(self):
        if self._last_name is None:
            self._last_name = self._fetch_field('last_name')
        return self._last_name

    @last_name.setter
    def last_name(self, x):
        if type(x) is str:
            self._last_name = x
        else:
            raise TypeError("User.last_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def deactivated(self):
        if self._deactivated is None:
            self._deactivated = self._fetch_field('deactivated')
        return self._deactivated

    @deactivated.setter
    def deactivated(self, x):
        if test_user_deactivated(x):
            self._deactivated = x
        else:
            raise TypeError("User.deactivated: cannot set attribute with value"
                            " of type `%s', `user_deactivated' expected" % x.__class__.__name__)

    @property
    def hidden(self):
        if self._hidden is None:
            self._hidden = self._fetch_field('hidden')
        return self._hidden

    @hidden.setter
    def hidden(self, x):
        if test_int1(x):
            self._hidden = x
        else:
            raise TypeError("User.hidden: cannot set attribute with value"
                            " of type `%s', `int1' expected" % x.__class__.__name__)

    @property
    def photo_id(self):
        if self._photo_id is None:
            self._photo_id = self._fetch_field('photo_id')
        return self._photo_id

    @photo_id.setter
    def photo_id(self, x):
        if type(x) is str:
            self._photo_id = x
        else:
            raise TypeError("User.photo_id: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("User.verified: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def blacklisted(self):
        if self._blacklisted is None:
            self._blacklisted = self._fetch_field('blacklisted')
        return self._blacklisted

    @blacklisted.setter
    def blacklisted(self, x):
        if test_flag(x):
            self._blacklisted = x
        else:
            raise TypeError("User.blacklisted: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def sex(self):
        if self._sex is None:
            self._sex = self._fetch_field('sex')
        return self._sex

    @sex.setter
    def sex(self, x):
        if test_int_0_1_2(x):
            self._sex = x
        else:
            raise TypeError("User.sex: cannot set attribute with value"
                            " of type `%s', `int_0_1_2' expected" % x.__class__.__name__)

    @property
    def bdate(self):
        if self._bdate is None:
            self._bdate = self._fetch_field('bdate')
        return self._bdate

    @bdate.setter
    def bdate(self, x):
        if type(x) is str:
            self._bdate = x
        else:
            raise TypeError("User.bdate: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def city(self):
        if self._city is None:
            self._city = self._fetch_field('city')
        return self._city

    @city.setter
    def city(self, x):
        if type(x) is Place:
            self._city = x
        else:
            raise TypeError("User.city: cannot set attribute with value"
                            " of type `%s', `Place' expected" % x.__class__.__name__)

    @property
    def country(self):
        if self._country is None:
            self._country = self._fetch_field('country')
        return self._country

    @country.setter
    def country(self, x):
        if type(x) is Place:
            self._country = x
        else:
            raise TypeError("User.country: cannot set attribute with value"
                            " of type `%s', `Place' expected" % x.__class__.__name__)

    @property
    def home_town(self):
        if self._home_town is None:
            self._home_town = self._fetch_field('home_town')
        return self._home_town

    @home_town.setter
    def home_town(self, x):
        if type(x) is str:
            self._home_town = x
        else:
            raise TypeError("User.home_town: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("User.photo_50: cannot set attribute with value"
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
            raise TypeError("User.photo_100: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_200_orig(self):
        if self._photo_200_orig is None:
            self._photo_200_orig = self._fetch_field('photo_200_orig')
        return self._photo_200_orig

    @photo_200_orig.setter
    def photo_200_orig(self, x):
        if type(x) is str:
            self._photo_200_orig = x
        else:
            raise TypeError("User.photo_200_orig: cannot set attribute with value"
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
            raise TypeError("User.photo_200: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_400_orig(self):
        if self._photo_400_orig is None:
            self._photo_400_orig = self._fetch_field('photo_400_orig')
        return self._photo_400_orig

    @photo_400_orig.setter
    def photo_400_orig(self, x):
        if type(x) is str:
            self._photo_400_orig = x
        else:
            raise TypeError("User.photo_400_orig: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_max(self):
        if self._photo_max is None:
            self._photo_max = self._fetch_field('photo_max')
        return self._photo_max

    @photo_max.setter
    def photo_max(self, x):
        if type(x) is str:
            self._photo_max = x
        else:
            raise TypeError("User.photo_max: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_max_orig(self):
        if self._photo_max_orig is None:
            self._photo_max_orig = self._fetch_field('photo_max_orig')
        return self._photo_max_orig

    @photo_max_orig.setter
    def photo_max_orig(self, x):
        if type(x) is str:
            self._photo_max_orig = x
        else:
            raise TypeError("User.photo_max_orig: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def online(self):
        if self._online is None:
            self._online = self._fetch_field('online')
        return self._online

    @online.setter
    def online(self, x):
        if test_flag(x):
            self._online = x
        else:
            raise TypeError("User.online: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def lists(self):
        if self._lists is None:
            self._lists = self._fetch_field('lists')
        return self._lists

    @lists.setter
    def lists(self, x):
        if type(x) is str:
            self._lists = x
        else:
            raise TypeError("User.lists: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def domain(self):
        if self._domain is None:
            self._domain = self._fetch_field('domain')
        return self._domain

    @domain.setter
    def domain(self, x):
        if type(x) is str:
            self._domain = x
        else:
            raise TypeError("User.domain: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def has_mobile(self):
        if self._has_mobile is None:
            self._has_mobile = self._fetch_field('has_mobile')
        return self._has_mobile

    @has_mobile.setter
    def has_mobile(self, x):
        if test_flag(x):
            self._has_mobile = x
        else:
            raise TypeError("User.has_mobile: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def contacts(self):
        if self._contacts is None:
            self._contacts = self._fetch_field('contacts')
        return self._contacts

    @contacts.setter
    def contacts(self, x):
        if type(x) is Contacts:
            self._contacts = x
        else:
            raise TypeError("User.contacts: cannot set attribute with value"
                            " of type `%s', `Contacts' expected" % x.__class__.__name__)

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
            raise TypeError("User.site: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def education(self):
        if self._education is None:
            self._education = self._fetch_field('education')
        return self._education

    @education.setter
    def education(self, x):
        if type(x) is Education:
            self._education = x
        else:
            raise TypeError("User.education: cannot set attribute with value"
                            " of type `%s', `Education' expected" % x.__class__.__name__)

    @property
    def universities(self):
        if self._universities is None:
            self._universities = self._fetch_field('universities')
        return self._universities

    @universities.setter
    def universities(self, x):
        if type(x) is University:
            self._universities = x
        else:
            raise TypeError("User.universities: cannot set attribute with value"
                            " of type `%s', `University' expected" % x.__class__.__name__)

    @property
    def schools(self):
        if self._schools is None:
            self._schools = self._fetch_field('schools')
        return self._schools

    @schools.setter
    def schools(self, x):
        if type(x) is School:
            self._schools = x
        else:
            raise TypeError("User.schools: cannot set attribute with value"
                            " of type `%s', `School' expected" % x.__class__.__name__)

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
            raise TypeError("User.status: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def last_seen(self):
        if self._last_seen is None:
            self._last_seen = self._fetch_field('last_seen')
        return self._last_seen

    @last_seen.setter
    def last_seen(self, x):
        if type(x) is LastSeen:
            self._last_seen = x
        else:
            raise TypeError("User.last_seen: cannot set attribute with value"
                            " of type `%s', `LastSeen' expected" % x.__class__.__name__)

    @property
    def followers_count(self):
        if self._followers_count is None:
            self._followers_count = self._fetch_field('followers_count')
        return self._followers_count

    @followers_count.setter
    def followers_count(self, x):
        if test_intp(x):
            self._followers_count = x
        else:
            raise TypeError("User.followers_count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def common_count(self):
        if self._common_count is None:
            self._common_count = self._fetch_field('common_count')
        return self._common_count

    @common_count.setter
    def common_count(self, x):
        if test_intp(x):
            self._common_count = x
        else:
            raise TypeError("User.common_count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def counters(self):
        if self._counters is None:
            self._counters = self._fetch_field('counters')
        return self._counters

    @counters.setter
    def counters(self, x):
        if type(x) is Counter:
            self._counters = x
        else:
            raise TypeError("User.counters: cannot set attribute with value"
                            " of type `%s', `Counter' expected" % x.__class__.__name__)

    @property
    def occupation(self):
        if self._occupation is None:
            self._occupation = self._fetch_field('occupation')
        return self._occupation

    @occupation.setter
    def occupation(self, x):
        if type(x) is Occupation:
            self._occupation = x
        else:
            raise TypeError("User.occupation: cannot set attribute with value"
                            " of type `%s', `Occupation' expected" % x.__class__.__name__)

    @property
    def nickname(self):
        if self._nickname is None:
            self._nickname = self._fetch_field('nickname')
        return self._nickname

    @nickname.setter
    def nickname(self, x):
        if type(x) is str:
            self._nickname = x
        else:
            raise TypeError("User.nickname: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def relatives(self):
        if self._relatives is None:
            self._relatives = self._fetch_field('relatives')
        return self._relatives

    @relatives.setter
    def relatives(self, x):
        if type(x) is Relative:
            self._relatives = x
        else:
            raise TypeError("User.relatives: cannot set attribute with value"
                            " of type `%s', `Relative' expected" % x.__class__.__name__)

    @property
    def relation(self):
        if self._relation is None:
            self._relation = self._fetch_field('relation')
        return self._relation

    @relation.setter
    def relation(self, x):
        if type(x) is Relation:
            self._relation = x
        else:
            raise TypeError("User.relation: cannot set attribute with value"
                            " of type `%s', `Relation' expected" % x.__class__.__name__)

    @property
    def personal(self):
        if self._personal is None:
            self._personal = self._fetch_field('personal')
        return self._personal

    @personal.setter
    def personal(self, x):
        if type(x) is Personal:
            self._personal = x
        else:
            raise TypeError("User.personal: cannot set attribute with value"
                            " of type `%s', `Personal' expected" % x.__class__.__name__)

    @property
    def connections(self):
        if self._connections is None:
            self._connections = self._fetch_field('connections')
        return self._connections

    @connections.setter
    def connections(self, x):
        if type(x) is str:
            self._connections = x
        else:
            raise TypeError("User.connections: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def twitter(self):
        if self._twitter is None:
            self._twitter = self._fetch_field('twitter')
        return self._twitter

    @twitter.setter
    def twitter(self, x):
        if type(x) is str:
            self._twitter = x
        else:
            raise TypeError("User.twitter: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def livejornal(self):
        if self._livejornal is None:
            self._livejornal = self._fetch_field('livejornal')
        return self._livejornal

    @livejornal.setter
    def livejornal(self, x):
        if type(x) is str:
            self._livejornal = x
        else:
            raise TypeError("User.livejornal: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def instagram(self):
        if self._instagram is None:
            self._instagram = self._fetch_field('instagram')
        return self._instagram

    @instagram.setter
    def instagram(self, x):
        if type(x) is str:
            self._instagram = x
        else:
            raise TypeError("User.instagram: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def skype(self):
        if self._skype is None:
            self._skype = self._fetch_field('skype')
        return self._skype

    @skype.setter
    def skype(self, x):
        if type(x) is str:
            self._skype = x
        else:
            raise TypeError("User.skype: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def facebook(self):
        if self._facebook is None:
            self._facebook = self._fetch_field('facebook')
        return self._facebook

    @facebook.setter
    def facebook(self, x):
        if type(x) is str:
            self._facebook = x
        else:
            raise TypeError("User.facebook: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def exports(self):
        if self._exports is None:
            self._exports = self._fetch_field('exports')
        return self._exports

    @exports.setter
    def exports(self, x):
        if type(x) is Export:
            self._exports = x
        else:
            raise TypeError("User.exports: cannot set attribute with value"
                            " of type `%s', `Export' expected" % x.__class__.__name__)

    @property
    def wall_comments(self):
        if self._wall_comments is None:
            self._wall_comments = self._fetch_field('wall_comments')
        return self._wall_comments

    @wall_comments.setter
    def wall_comments(self, x):
        if test_flag(x):
            self._wall_comments = x
        else:
            raise TypeError("User.wall_comments: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def activities(self):
        if self._activities is None:
            self._activities = self._fetch_field('activities')
        return self._activities

    @activities.setter
    def activities(self, x):
        if type(x) is str:
            self._activities = x
        else:
            raise TypeError("User.activities: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def interests(self):
        if self._interests is None:
            self._interests = self._fetch_field('interests')
        return self._interests

    @interests.setter
    def interests(self, x):
        if type(x) is str:
            self._interests = x
        else:
            raise TypeError("User.interests: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def music(self):
        if self._music is None:
            self._music = self._fetch_field('music')
        return self._music

    @music.setter
    def music(self, x):
        if type(x) is str:
            self._music = x
        else:
            raise TypeError("User.music: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def movies(self):
        if self._movies is None:
            self._movies = self._fetch_field('movies')
        return self._movies

    @movies.setter
    def movies(self, x):
        if type(x) is str:
            self._movies = x
        else:
            raise TypeError("User.movies: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def tv(self):
        if self._tv is None:
            self._tv = self._fetch_field('tv')
        return self._tv

    @tv.setter
    def tv(self, x):
        if type(x) is str:
            self._tv = x
        else:
            raise TypeError("User.tv: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def books(self):
        if self._books is None:
            self._books = self._fetch_field('books')
        return self._books

    @books.setter
    def books(self, x):
        if type(x) is str:
            self._books = x
        else:
            raise TypeError("User.books: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def games(self):
        if self._games is None:
            self._games = self._fetch_field('games')
        return self._games

    @games.setter
    def games(self, x):
        if type(x) is str:
            self._games = x
        else:
            raise TypeError("User.games: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def about(self):
        if self._about is None:
            self._about = self._fetch_field('about')
        return self._about

    @about.setter
    def about(self, x):
        if type(x) is str:
            self._about = x
        else:
            raise TypeError("User.about: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def quotes(self):
        if self._quotes is None:
            self._quotes = self._fetch_field('quotes')
        return self._quotes

    @quotes.setter
    def quotes(self, x):
        if type(x) is str:
            self._quotes = x
        else:
            raise TypeError("User.quotes: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("User.can_post: cannot set attribute with value"
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
            raise TypeError("User.can_see_all_posts: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_see_audio(self):
        if self._can_see_audio is None:
            self._can_see_audio = self._fetch_field('can_see_audio')
        return self._can_see_audio

    @can_see_audio.setter
    def can_see_audio(self, x):
        if test_flag(x):
            self._can_see_audio = x
        else:
            raise TypeError("User.can_see_audio: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_write_private_message(self):
        if self._can_write_private_message is None:
            self._can_write_private_message = self._fetch_field('can_write_private_message')
        return self._can_write_private_message

    @can_write_private_message.setter
    def can_write_private_message(self, x):
        if test_flag(x):
            self._can_write_private_message = x
        else:
            raise TypeError("User.can_write_private_message: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def can_send_friend_request(self):
        if self._can_send_friend_request is None:
            self._can_send_friend_request = self._fetch_field('can_send_friend_request')
        return self._can_send_friend_request

    @can_send_friend_request.setter
    def can_send_friend_request(self, x):
        if test_flag(x):
            self._can_send_friend_request = x
        else:
            raise TypeError("User.can_send_friend_request: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

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
            raise TypeError("User.is_favorite: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def timezone(self):
        if self._timezone is None:
            self._timezone = self._fetch_field('timezone')
        return self._timezone

    @timezone.setter
    def timezone(self, x):
        if test_intp(x):
            self._timezone = x
        else:
            raise TypeError("User.timezone: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

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
            raise TypeError("User.screen_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def maiden_name(self):
        if self._maiden_name is None:
            self._maiden_name = self._fetch_field('maiden_name')
        return self._maiden_name

    @maiden_name.setter
    def maiden_name(self, x):
        if type(x) is str:
            self._maiden_name = x
        else:
            raise TypeError("User.maiden_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def crop_photo(self):
        if self._crop_photo is None:
            self._crop_photo = self._fetch_field('crop_photo')
        return self._crop_photo

    @crop_photo.setter
    def crop_photo(self, x):
        if type(x) is Crop:
            self._crop_photo = x
        else:
            raise TypeError("User.crop_photo: cannot set attribute with value"
                            " of type `%s', `Crop' expected" % x.__class__.__name__)

    @property
    def is_friend(self):
        if self._is_friend is None:
            self._is_friend = self._fetch_field('is_friend')
        return self._is_friend

    @is_friend.setter
    def is_friend(self, x):
        if test_int_1_2(x):
            self._is_friend = x
        else:
            raise TypeError("User.is_friend: cannot set attribute with value"
                            " of type `%s', `int_1_2' expected" % x.__class__.__name__)

    @property
    def friend_status(self):
        if self._friend_status is None:
            self._friend_status = self._fetch_field('friend_status')
        return self._friend_status

    @friend_status.setter
    def friend_status(self, x):
        if test_int_0_1_2_3(x):
            self._friend_status = x
        else:
            raise TypeError("User.friend_status: cannot set attribute with value"
                            " of type `%s', `int_0_1_2_3' expected" % x.__class__.__name__)


class Place(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'title')
        self.__attrs_required__ = set(['id', 'title'])

        super(Place, self).__init__(**kwargs)

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
            raise TypeError("Place.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Place.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Contacts(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('mobile_phone', 'home_phone')
        self.__attrs_required__ = set()

        super(Contacts, self).__init__(**kwargs)

    @property
    def mobile_phone(self):
        if self._mobile_phone is None:
            self._mobile_phone = self._fetch_field('mobile_phone')
        return self._mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, x):
        if type(x) is str:
            self._mobile_phone = x
        else:
            raise TypeError("Contacts.mobile_phone: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def home_phone(self):
        if self._home_phone is None:
            self._home_phone = self._fetch_field('home_phone')
        return self._home_phone

    @home_phone.setter
    def home_phone(self, x):
        if type(x) is str:
            self._home_phone = x
        else:
            raise TypeError("Contacts.home_phone: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Education(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('unversity', 'unversity_name', 'faculty',
        'faculty_name', 'graduation')
        self.__attrs_required__ = set()

        super(Education, self).__init__(**kwargs)

    @property
    def unversity(self):
        if self._unversity is None:
            self._unversity = self._fetch_field('unversity')
        return self._unversity

    @unversity.setter
    def unversity(self, x):
        if test_intp(x):
            self._unversity = x
        else:
            raise TypeError("Education.unversity: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def unversity_name(self):
        if self._unversity_name is None:
            self._unversity_name = self._fetch_field('unversity_name')
        return self._unversity_name

    @unversity_name.setter
    def unversity_name(self, x):
        if type(x) is str:
            self._unversity_name = x
        else:
            raise TypeError("Education.unversity_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def faculty(self):
        if self._faculty is None:
            self._faculty = self._fetch_field('faculty')
        return self._faculty

    @faculty.setter
    def faculty(self, x):
        if test_intp(x):
            self._faculty = x
        else:
            raise TypeError("Education.faculty: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def faculty_name(self):
        if self._faculty_name is None:
            self._faculty_name = self._fetch_field('faculty_name')
        return self._faculty_name

    @faculty_name.setter
    def faculty_name(self, x):
        if type(x) is str:
            self._faculty_name = x
        else:
            raise TypeError("Education.faculty_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def graduation(self):
        if self._graduation is None:
            self._graduation = self._fetch_field('graduation')
        return self._graduation

    @graduation.setter
    def graduation(self, x):
        if test_intp(x):
            self._graduation = x
        else:
            raise TypeError("Education.graduation: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class University(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'country', 'city', 'name', 'faculty',
        'faculty_name', 'chair', 'chair_name', 'graduation')
        self.__attrs_required__ = set(['id', 'country', 'city', 'name'])

        super(University, self).__init__(**kwargs)

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
            raise TypeError("University.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def country(self):
        if self._country is None:
            self._country = self._fetch_field('country')
        return self._country

    @country.setter
    def country(self, x):
        if test_intp(x):
            self._country = x
        else:
            raise TypeError("University.country: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def city(self):
        if self._city is None:
            self._city = self._fetch_field('city')
        return self._city

    @city.setter
    def city(self, x):
        if test_intp(x):
            self._city = x
        else:
            raise TypeError("University.city: cannot set attribute with value"
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
            raise TypeError("University.name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def faculty(self):
        if self._faculty is None:
            self._faculty = self._fetch_field('faculty')
        return self._faculty

    @faculty.setter
    def faculty(self, x):
        if test_intp(x):
            self._faculty = x
        else:
            raise TypeError("University.faculty: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def faculty_name(self):
        if self._faculty_name is None:
            self._faculty_name = self._fetch_field('faculty_name')
        return self._faculty_name

    @faculty_name.setter
    def faculty_name(self, x):
        if type(x) is str:
            self._faculty_name = x
        else:
            raise TypeError("University.faculty_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def chair(self):
        if self._chair is None:
            self._chair = self._fetch_field('chair')
        return self._chair

    @chair.setter
    def chair(self, x):
        if type(x) is int:
            self._chair = x
        else:
            raise TypeError("University.chair: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def chair_name(self):
        if self._chair_name is None:
            self._chair_name = self._fetch_field('chair_name')
        return self._chair_name

    @chair_name.setter
    def chair_name(self, x):
        if type(x) is str:
            self._chair_name = x
        else:
            raise TypeError("University.chair_name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def graduation(self):
        if self._graduation is None:
            self._graduation = self._fetch_field('graduation')
        return self._graduation

    @graduation.setter
    def graduation(self, x):
        if test_intp(x):
            self._graduation = x
        else:
            raise TypeError("University.graduation: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class School(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'country', 'city', 'name', 'year_from',
        'year_to', 'year_graduated', 'class', 'type', 'type_str')
        self.__attrs_required__ = set(['id', 'country', 'city', 'name'])

        super(School, self).__init__(**kwargs)

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
            raise TypeError("School.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def country(self):
        if self._country is None:
            self._country = self._fetch_field('country')
        return self._country

    @country.setter
    def country(self, x):
        if test_intp(x):
            self._country = x
        else:
            raise TypeError("School.country: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def city(self):
        if self._city is None:
            self._city = self._fetch_field('city')
        return self._city

    @city.setter
    def city(self, x):
        if test_intp(x):
            self._city = x
        else:
            raise TypeError("School.city: cannot set attribute with value"
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
            raise TypeError("School.name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def year_from(self):
        if self._year_from is None:
            self._year_from = self._fetch_field('year_from')
        return self._year_from

    @year_from.setter
    def year_from(self, x):
        if test_intp(x):
            self._year_from = x
        else:
            raise TypeError("School.year_from: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def year_to(self):
        if self._year_to is None:
            self._year_to = self._fetch_field('year_to')
        return self._year_to

    @year_to.setter
    def year_to(self, x):
        if test_intp(x):
            self._year_to = x
        else:
            raise TypeError("School.year_to: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def year_graduated(self):
        if self._year_graduated is None:
            self._year_graduated = self._fetch_field('year_graduated')
        return self._year_graduated

    @year_graduated.setter
    def year_graduated(self, x):
        if test_intp(x):
            self._year_graduated = x
        else:
            raise TypeError("School.year_graduated: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def class(self):
        if self._class is None:
            self._class = self._fetch_field('class')
        return self._class

    @class.setter
    def class(self, x):
        if type(x) is str:
            self._class = x
        else:
            raise TypeError("School.class: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if test_intp(x):
            self._type = x
        else:
            raise TypeError("School.type: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def type_str(self):
        if self._type_str is None:
            self._type_str = self._fetch_field('type_str')
        return self._type_str

    @type_str.setter
    def type_str(self, x):
        if type(x) is str:
            self._type_str = x
        else:
            raise TypeError("School.type_str: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Counter(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('albums', 'videos', 'audios', 'photos', 'notes',
        'friends', 'groups', 'online_friends', 'mutual_friends', 'user_videos',
        'followers', 'user_photos', 'subscriptions')
        self.__attrs_required__ = set()

        super(Counter, self).__init__(**kwargs)

    @property
    def albums(self):
        if self._albums is None:
            self._albums = self._fetch_field('albums')
        return self._albums

    @albums.setter
    def albums(self, x):
        if test_intp(x):
            self._albums = x
        else:
            raise TypeError("Counter.albums: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def videos(self):
        if self._videos is None:
            self._videos = self._fetch_field('videos')
        return self._videos

    @videos.setter
    def videos(self, x):
        if test_intp(x):
            self._videos = x
        else:
            raise TypeError("Counter.videos: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def audios(self):
        if self._audios is None:
            self._audios = self._fetch_field('audios')
        return self._audios

    @audios.setter
    def audios(self, x):
        if test_intp(x):
            self._audios = x
        else:
            raise TypeError("Counter.audios: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def photos(self):
        if self._photos is None:
            self._photos = self._fetch_field('photos')
        return self._photos

    @photos.setter
    def photos(self, x):
        if test_intp(x):
            self._photos = x
        else:
            raise TypeError("Counter.photos: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def notes(self):
        if self._notes is None:
            self._notes = self._fetch_field('notes')
        return self._notes

    @notes.setter
    def notes(self, x):
        if test_intp(x):
            self._notes = x
        else:
            raise TypeError("Counter.notes: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def friends(self):
        if self._friends is None:
            self._friends = self._fetch_field('friends')
        return self._friends

    @friends.setter
    def friends(self, x):
        if test_intp(x):
            self._friends = x
        else:
            raise TypeError("Counter.friends: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def groups(self):
        if self._groups is None:
            self._groups = self._fetch_field('groups')
        return self._groups

    @groups.setter
    def groups(self, x):
        if test_intp(x):
            self._groups = x
        else:
            raise TypeError("Counter.groups: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def online_friends(self):
        if self._online_friends is None:
            self._online_friends = self._fetch_field('online_friends')
        return self._online_friends

    @online_friends.setter
    def online_friends(self, x):
        if test_intp(x):
            self._online_friends = x
        else:
            raise TypeError("Counter.online_friends: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def mutual_friends(self):
        if self._mutual_friends is None:
            self._mutual_friends = self._fetch_field('mutual_friends')
        return self._mutual_friends

    @mutual_friends.setter
    def mutual_friends(self, x):
        if test_intp(x):
            self._mutual_friends = x
        else:
            raise TypeError("Counter.mutual_friends: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_videos(self):
        if self._user_videos is None:
            self._user_videos = self._fetch_field('user_videos')
        return self._user_videos

    @user_videos.setter
    def user_videos(self, x):
        if test_intp(x):
            self._user_videos = x
        else:
            raise TypeError("Counter.user_videos: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def followers(self):
        if self._followers is None:
            self._followers = self._fetch_field('followers')
        return self._followers

    @followers.setter
    def followers(self, x):
        if test_intp(x):
            self._followers = x
        else:
            raise TypeError("Counter.followers: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_photos(self):
        if self._user_photos is None:
            self._user_photos = self._fetch_field('user_photos')
        return self._user_photos

    @user_photos.setter
    def user_photos(self, x):
        if test_intp(x):
            self._user_photos = x
        else:
            raise TypeError("Counter.user_photos: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def subscriptions(self):
        if self._subscriptions is None:
            self._subscriptions = self._fetch_field('subscriptions')
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, x):
        if test_intp(x):
            self._subscriptions = x
        else:
            raise TypeError("Counter.subscriptions: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Occupation(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('type', 'id', 'name')
        self.__attrs_required__ = set()

        super(Occupation, self).__init__(**kwargs)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if test_occupation_type(x):
            self._type = x
        else:
            raise TypeError("Occupation.type: cannot set attribute with value"
                            " of type `%s', `occupation_type' expected" % x.__class__.__name__)

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
            raise TypeError("Occupation.id: cannot set attribute with value"
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
            raise TypeError("Occupation.name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Relation(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('relation', 'relation_partner')
        self.__attrs_required__ = set()

        super(Relation, self).__init__(**kwargs)

    @property
    def relation(self):
        if self._relation is None:
            self._relation = self._fetch_field('relation')
        return self._relation

    @relation.setter
    def relation(self, x):
        if test_relation_int(x):
            self._relation = x
        else:
            raise TypeError("Relation.relation: cannot set attribute with value"
                            " of type `%s', `relation_int' expected" % x.__class__.__name__)

    @property
    def relation_partner(self):
        if self._relation_partner is None:
            self._relation_partner = self._fetch_field('relation_partner')
        return self._relation_partner

    @relation_partner.setter
    def relation_partner(self, x):
        if type(x) is Person:
            self._relation_partner = x
        else:
            raise TypeError("Relation.relation_partner: cannot set attribute with value"
                            " of type `%s', `Person' expected" % x.__class__.__name__)


class Person(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'name')
        self.__attrs_required__ = set(['id'])

        super(Person, self).__init__(**kwargs)

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
            raise TypeError("Person.id: cannot set attribute with value"
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
            raise TypeError("Person.name: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Personal(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('political', 'langs', 'religion', 'inspired_by',
        'people_main', 'life_main', 'smoking', 'alkochol')
        self.__attrs_required__ = set()

        super(Personal, self).__init__(**kwargs)

    @property
    def political(self):
        if self._political is None:
            self._political = self._fetch_field('political')
        return self._political

    @political.setter
    def political(self, x):
        if test_political(x):
            self._political = x
        else:
            raise TypeError("Personal.political: cannot set attribute with value"
                            " of type `%s', `political' expected" % x.__class__.__name__)

    @property
    def langs(self):
        if self._langs is None:
            self._langs = self._fetch_field('langs')
        return self._langs

    @langs.setter
    def langs(self, x):
        if type(x) is str:
            self._langs = x
        else:
            raise TypeError("Personal.langs: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def religion(self):
        if self._religion is None:
            self._religion = self._fetch_field('religion')
        return self._religion

    @religion.setter
    def religion(self, x):
        if type(x) is str:
            self._religion = x
        else:
            raise TypeError("Personal.religion: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def inspired_by(self):
        if self._inspired_by is None:
            self._inspired_by = self._fetch_field('inspired_by')
        return self._inspired_by

    @inspired_by.setter
    def inspired_by(self, x):
        if type(x) is str:
            self._inspired_by = x
        else:
            raise TypeError("Personal.inspired_by: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def people_main(self):
        if self._people_main is None:
            self._people_main = self._fetch_field('people_main')
        return self._people_main

    @people_main.setter
    def people_main(self, x):
        if test_people_main(x):
            self._people_main = x
        else:
            raise TypeError("Personal.people_main: cannot set attribute with value"
                            " of type `%s', `people_main' expected" % x.__class__.__name__)

    @property
    def life_main(self):
        if self._life_main is None:
            self._life_main = self._fetch_field('life_main')
        return self._life_main

    @life_main.setter
    def life_main(self, x):
        if test_life_main(x):
            self._life_main = x
        else:
            raise TypeError("Personal.life_main: cannot set attribute with value"
                            " of type `%s', `life_main' expected" % x.__class__.__name__)

    @property
    def smoking(self):
        if self._smoking is None:
            self._smoking = self._fetch_field('smoking')
        return self._smoking

    @smoking.setter
    def smoking(self, x):
        if test_view(x):
            self._smoking = x
        else:
            raise TypeError("Personal.smoking: cannot set attribute with value"
                            " of type `%s', `view' expected" % x.__class__.__name__)

    @property
    def alkochol(self):
        if self._alkochol is None:
            self._alkochol = self._fetch_field('alkochol')
        return self._alkochol

    @alkochol.setter
    def alkochol(self, x):
        if test_view(x):
            self._alkochol = x
        else:
            raise TypeError("Personal.alkochol: cannot set attribute with value"
                            " of type `%s', `view' expected" % x.__class__.__name__)


class Export(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('twitter', 'instagram', 'facebook', 'livejournal')
        self.__attrs_required__ = set()

        super(Export, self).__init__(**kwargs)

    @property
    def twitter(self):
        if self._twitter is None:
            self._twitter = self._fetch_field('twitter')
        return self._twitter

    @twitter.setter
    def twitter(self, x):
        if test_flag(x):
            self._twitter = x
        else:
            raise TypeError("Export.twitter: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def instagram(self):
        if self._instagram is None:
            self._instagram = self._fetch_field('instagram')
        return self._instagram

    @instagram.setter
    def instagram(self, x):
        if test_flag(x):
            self._instagram = x
        else:
            raise TypeError("Export.instagram: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def facebook(self):
        if self._facebook is None:
            self._facebook = self._fetch_field('facebook')
        return self._facebook

    @facebook.setter
    def facebook(self, x):
        if test_flag(x):
            self._facebook = x
        else:
            raise TypeError("Export.facebook: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def livejournal(self):
        if self._livejournal is None:
            self._livejournal = self._fetch_field('livejournal')
        return self._livejournal

    @livejournal.setter
    def livejournal(self, x):
        if test_flag(x):
            self._livejournal = x
        else:
            raise TypeError("Export.livejournal: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)


class Crop(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('photo', 'crop', 'rect')
        self.__attrs_required__ = set()

        super(Crop, self).__init__(**kwargs)

    @property
    def photo(self):
        if self._photo is None:
            self._photo = self._fetch_field('photo')
        return self._photo

    @photo.setter
    def photo(self, x):
        if type(x) is Photo:
            self._photo = x
        else:
            raise TypeError("Crop.photo: cannot set attribute with value"
                            " of type `%s', `Photo' expected" % x.__class__.__name__)

    @property
    def crop(self):
        if self._crop is None:
            self._crop = self._fetch_field('crop')
        return self._crop

    @crop.setter
    def crop(self, x):
        if type(x) is Coordinate:
            self._crop = x
        else:
            raise TypeError("Crop.crop: cannot set attribute with value"
                            " of type `%s', `Coordinate' expected" % x.__class__.__name__)

    @property
    def rect(self):
        if self._rect is None:
            self._rect = self._fetch_field('rect')
        return self._rect

    @rect.setter
    def rect(self, x):
        if type(x) is Coordinate:
            self._rect = x
        else:
            raise TypeError("Crop.rect: cannot set attribute with value"
                            " of type `%s', `Coordinate' expected" % x.__class__.__name__)


class Coordinate(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('x', 'y', 'y1', 'y2')
        self.__attrs_required__ = set(['x', 'y', 'y1', 'y2'])

        super(Coordinate, self).__init__(**kwargs)

    @property
    def x(self):
        if self._x is None:
            self._x = self._fetch_field('x')
        return self._x

    @x.setter
    def x(self, x):
        if type(x) is float:
            self._x = x
        else:
            raise TypeError("Coordinate.x: cannot set attribute with value"
                            " of type `%s', `float' expected" % x.__class__.__name__)

    @property
    def y(self):
        if self._y is None:
            self._y = self._fetch_field('y')
        return self._y

    @y.setter
    def y(self, x):
        if type(x) is float:
            self._y = x
        else:
            raise TypeError("Coordinate.y: cannot set attribute with value"
                            " of type `%s', `float' expected" % x.__class__.__name__)

    @property
    def y1(self):
        if self._y1 is None:
            self._y1 = self._fetch_field('y1')
        return self._y1

    @y1.setter
    def y1(self, x):
        if type(x) is float:
            self._y1 = x
        else:
            raise TypeError("Coordinate.y1: cannot set attribute with value"
                            " of type `%s', `float' expected" % x.__class__.__name__)

    @property
    def y2(self):
        if self._y2 is None:
            self._y2 = self._fetch_field('y2')
        return self._y2

    @y2.setter
    def y2(self, x):
        if type(x) is float:
            self._y2 = x
        else:
            raise TypeError("Coordinate.y2: cannot set attribute with value"
                            " of type `%s', `float' expected" % x.__class__.__name__)


class Photo(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'album_id', 'owner_id', 'user_id', 'photo_75',
        'photo_130', 'photo_604', 'photo_807', 'photo_1280', 'photo_2560',
        'width', 'height', 'text', 'date')
        self.__attrs_required__ = set(['id', 'album_id', 'owner_id', 'user_id'])

        super(Photo, self).__init__(**kwargs)

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
            raise TypeError("Photo.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def album_id(self):
        if self._album_id is None:
            self._album_id = self._fetch_field('album_id')
        return self._album_id

    @album_id.setter
    def album_id(self, x):
        if type(x) is int:
            self._album_id = x
        else:
            raise TypeError("Photo.album_id: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

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
            raise TypeError("Photo.owner_id: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def user_id(self):
        if self._user_id is None:
            self._user_id = self._fetch_field('user_id')
        return self._user_id

    @user_id.setter
    def user_id(self, x):
        if test_intp(x):
            self._user_id = x
        else:
            raise TypeError("Photo.user_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def photo_75(self):
        if self._photo_75 is None:
            self._photo_75 = self._fetch_field('photo_75')
        return self._photo_75

    @photo_75.setter
    def photo_75(self, x):
        if type(x) is str:
            self._photo_75 = x
        else:
            raise TypeError("Photo.photo_75: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_130(self):
        if self._photo_130 is None:
            self._photo_130 = self._fetch_field('photo_130')
        return self._photo_130

    @photo_130.setter
    def photo_130(self, x):
        if type(x) is str:
            self._photo_130 = x
        else:
            raise TypeError("Photo.photo_130: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_604(self):
        if self._photo_604 is None:
            self._photo_604 = self._fetch_field('photo_604')
        return self._photo_604

    @photo_604.setter
    def photo_604(self, x):
        if type(x) is str:
            self._photo_604 = x
        else:
            raise TypeError("Photo.photo_604: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_807(self):
        if self._photo_807 is None:
            self._photo_807 = self._fetch_field('photo_807')
        return self._photo_807

    @photo_807.setter
    def photo_807(self, x):
        if type(x) is str:
            self._photo_807 = x
        else:
            raise TypeError("Photo.photo_807: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_1280(self):
        if self._photo_1280 is None:
            self._photo_1280 = self._fetch_field('photo_1280')
        return self._photo_1280

    @photo_1280.setter
    def photo_1280(self, x):
        if type(x) is str:
            self._photo_1280 = x
        else:
            raise TypeError("Photo.photo_1280: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_2560(self):
        if self._photo_2560 is None:
            self._photo_2560 = self._fetch_field('photo_2560')
        return self._photo_2560

    @photo_2560.setter
    def photo_2560(self, x):
        if type(x) is str:
            self._photo_2560 = x
        else:
            raise TypeError("Photo.photo_2560: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def width(self):
        if self._width is None:
            self._width = self._fetch_field('width')
        return self._width

    @width.setter
    def width(self, x):
        if test_intp(x):
            self._width = x
        else:
            raise TypeError("Photo.width: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def height(self):
        if self._height is None:
            self._height = self._fetch_field('height')
        return self._height

    @height.setter
    def height(self, x):
        if test_intp(x):
            self._height = x
        else:
            raise TypeError("Photo.height: cannot set attribute with value"
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
            raise TypeError("Photo.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Photo.date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Audio(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'artist', 'title', 'duration',
        'url', 'lyrics_id', 'album_id', 'genre_id')
        self.__attrs_required__ = set(['id', 'owner_id', 'duration'])

        super(Audio, self).__init__(**kwargs)

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
            raise TypeError("Audio.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("Audio.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def artist(self):
        if self._artist is None:
            self._artist = self._fetch_field('artist')
        return self._artist

    @artist.setter
    def artist(self, x):
        if type(x) is str:
            self._artist = x
        else:
            raise TypeError("Audio.artist: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Audio.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def duration(self):
        if self._duration is None:
            self._duration = self._fetch_field('duration')
        return self._duration

    @duration.setter
    def duration(self, x):
        if test_intp(x):
            self._duration = x
        else:
            raise TypeError("Audio.duration: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

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
            raise TypeError("Audio.url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def lyrics_id(self):
        if self._lyrics_id is None:
            self._lyrics_id = self._fetch_field('lyrics_id')
        return self._lyrics_id

    @lyrics_id.setter
    def lyrics_id(self, x):
        if test_intp(x):
            self._lyrics_id = x
        else:
            raise TypeError("Audio.lyrics_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def album_id(self):
        if self._album_id is None:
            self._album_id = self._fetch_field('album_id')
        return self._album_id

    @album_id.setter
    def album_id(self, x):
        if test_intp(x):
            self._album_id = x
        else:
            raise TypeError("Audio.album_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def genre_id(self):
        if self._genre_id is None:
            self._genre_id = self._fetch_field('genre_id')
        return self._genre_id

    @genre_id.setter
    def genre_id(self, x):
        if test_intp(x):
            self._genre_id = x
        else:
            raise TypeError("Audio.genre_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Video(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'title', 'description', 'duration',
        'link', 'photo_130', 'photo_320', 'photo_640', 'date', 'adding_date',
        'views', 'comments', 'player', 'processing')
        self.__attrs_required__ = set(['id', 'owner_id'])

        super(Video, self).__init__(**kwargs)

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
            raise TypeError("Video.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("Video.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Video.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Video.description: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def duration(self):
        if self._duration is None:
            self._duration = self._fetch_field('duration')
        return self._duration

    @duration.setter
    def duration(self, x):
        if test_intp(x):
            self._duration = x
        else:
            raise TypeError("Video.duration: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def link(self):
        if self._link is None:
            self._link = self._fetch_field('link')
        return self._link

    @link.setter
    def link(self, x):
        if type(x) is str:
            self._link = x
        else:
            raise TypeError("Video.link: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_130(self):
        if self._photo_130 is None:
            self._photo_130 = self._fetch_field('photo_130')
        return self._photo_130

    @photo_130.setter
    def photo_130(self, x):
        if type(x) is str:
            self._photo_130 = x
        else:
            raise TypeError("Video.photo_130: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_320(self):
        if self._photo_320 is None:
            self._photo_320 = self._fetch_field('photo_320')
        return self._photo_320

    @photo_320.setter
    def photo_320(self, x):
        if type(x) is str:
            self._photo_320 = x
        else:
            raise TypeError("Video.photo_320: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_640(self):
        if self._photo_640 is None:
            self._photo_640 = self._fetch_field('photo_640')
        return self._photo_640

    @photo_640.setter
    def photo_640(self, x):
        if type(x) is str:
            self._photo_640 = x
        else:
            raise TypeError("Video.photo_640: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Video.date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def adding_date(self):
        if self._adding_date is None:
            self._adding_date = self._fetch_field('adding_date')
        return self._adding_date

    @adding_date.setter
    def adding_date(self, x):
        if test_intp(x):
            self._adding_date = x
        else:
            raise TypeError("Video.adding_date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def views(self):
        if self._views is None:
            self._views = self._fetch_field('views')
        return self._views

    @views.setter
    def views(self, x):
        if test_intp(x):
            self._views = x
        else:
            raise TypeError("Video.views: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def comments(self):
        if self._comments is None:
            self._comments = self._fetch_field('comments')
        return self._comments

    @comments.setter
    def comments(self, x):
        if test_intp(x):
            self._comments = x
        else:
            raise TypeError("Video.comments: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def player(self):
        if self._player is None:
            self._player = self._fetch_field('player')
        return self._player

    @player.setter
    def player(self, x):
        if type(x) is str:
            self._player = x
        else:
            raise TypeError("Video.player: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def processing(self):
        if self._processing is None:
            self._processing = self._fetch_field('processing')
        return self._processing

    @processing.setter
    def processing(self, x):
        if test_intp(x):
            self._processing = x
        else:
            raise TypeError("Video.processing: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Document(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'title', 'size', 'ext', 'url',
        'photo_100', 'photo_130')
        self.__attrs_required__ = set(['id', 'owner_id', 'size', 'ext', 'url'])

        super(Document, self).__init__(**kwargs)

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
            raise TypeError("Document.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("Document.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Document.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def size(self):
        if self._size is None:
            self._size = self._fetch_field('size')
        return self._size

    @size.setter
    def size(self, x):
        if test_intp(x):
            self._size = x
        else:
            raise TypeError("Document.size: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def ext(self):
        if self._ext is None:
            self._ext = self._fetch_field('ext')
        return self._ext

    @ext.setter
    def ext(self, x):
        if type(x) is str:
            self._ext = x
        else:
            raise TypeError("Document.ext: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Document.url: cannot set attribute with value"
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
            raise TypeError("Document.photo_100: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_130(self):
        if self._photo_130 is None:
            self._photo_130 = self._fetch_field('photo_130')
        return self._photo_130

    @photo_130.setter
    def photo_130(self, x):
        if type(x) is str:
            self._photo_130 = x
        else:
            raise TypeError("Document.photo_130: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Message(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'user_id', 'from_id', 'date', 'read_state',
        'out', 'title', 'body', 'geo', 'attachments', 'fwd_messages', 'emoji',
        'important', 'deleted', 'chat_id', 'chat_active', 'push_settings',
        'users_count', 'admin_id', 'action', 'action_mid', 'action_email',
        'action_text', 'photo_50', 'photo_100', 'photo_200')
        self.__attrs_required__ = set(['id', 'user_id', 'from_id', 'date', 'read_state', 'out', 'title', 'body', 'emoji', 'important', 'deleted'])

        super(Message, self).__init__(**kwargs)

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
            raise TypeError("Message.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_id(self):
        if self._user_id is None:
            self._user_id = self._fetch_field('user_id')
        return self._user_id

    @user_id.setter
    def user_id(self, x):
        if test_intp(x):
            self._user_id = x
        else:
            raise TypeError("Message.user_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def from_id(self):
        if self._from_id is None:
            self._from_id = self._fetch_field('from_id')
        return self._from_id

    @from_id.setter
    def from_id(self, x):
        if test_intp(x):
            self._from_id = x
        else:
            raise TypeError("Message.from_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

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
            raise TypeError("Message.date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def read_state(self):
        if self._read_state is None:
            self._read_state = self._fetch_field('read_state')
        return self._read_state

    @read_state.setter
    def read_state(self, x):
        if test_flag(x):
            self._read_state = x
        else:
            raise TypeError("Message.read_state: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def out(self):
        if self._out is None:
            self._out = self._fetch_field('out')
        return self._out

    @out.setter
    def out(self, x):
        if test_flag(x):
            self._out = x
        else:
            raise TypeError("Message.out: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Message.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def body(self):
        if self._body is None:
            self._body = self._fetch_field('body')
        return self._body

    @body.setter
    def body(self, x):
        if type(x) is str:
            self._body = x
        else:
            raise TypeError("Message.body: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Message.geo: cannot set attribute with value"
                            " of type `%s', `Geo' expected" % x.__class__.__name__)

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = self._fetch_field('attachments')
        return self._attachments

    @attachments.setter
    def attachments(self, x):
        if type(x) is Attachment_m:
            self._attachments = x
        else:
            raise TypeError("Message.attachments: cannot set attribute with value"
                            " of type `%s', `Attachment_m' expected" % x.__class__.__name__)

    @property
    def fwd_messages(self):
        if self._fwd_messages is None:
            self._fwd_messages = self._fetch_field('fwd_messages')
        return self._fwd_messages

    @fwd_messages.setter
    def fwd_messages(self, x):
        if type(x) is Message:
            self._fwd_messages = x
        else:
            raise TypeError("Message.fwd_messages: cannot set attribute with value"
                            " of type `%s', `Message' expected" % x.__class__.__name__)

    @property
    def emoji(self):
        if self._emoji is None:
            self._emoji = self._fetch_field('emoji')
        return self._emoji

    @emoji.setter
    def emoji(self, x):
        if test_flag(x):
            self._emoji = x
        else:
            raise TypeError("Message.emoji: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def important(self):
        if self._important is None:
            self._important = self._fetch_field('important')
        return self._important

    @important.setter
    def important(self, x):
        if test_flag(x):
            self._important = x
        else:
            raise TypeError("Message.important: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def deleted(self):
        if self._deleted is None:
            self._deleted = self._fetch_field('deleted')
        return self._deleted

    @deleted.setter
    def deleted(self, x):
        if test_flag(x):
            self._deleted = x
        else:
            raise TypeError("Message.deleted: cannot set attribute with value"
                            " of type `%s', `flag' expected" % x.__class__.__name__)

    @property
    def chat_id(self):
        if self._chat_id is None:
            self._chat_id = self._fetch_field('chat_id')
        return self._chat_id

    @chat_id.setter
    def chat_id(self, x):
        if test_intp(x):
            self._chat_id = x
        else:
            raise TypeError("Message.chat_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def chat_active(self):
        if self._chat_active is None:
            self._chat_active = self._fetch_field('chat_active')
        return self._chat_active

    @chat_active.setter
    def chat_active(self, x):
        if type(x) is str:
            self._chat_active = x
        else:
            raise TypeError("Message.chat_active: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def push_settings(self):
        if self._push_settings is None:
            self._push_settings = self._fetch_field('push_settings')
        return self._push_settings

    @push_settings.setter
    def push_settings(self, x):
        if test_push_settings(x):
            self._push_settings = x
        else:
            raise TypeError("Message.push_settings: cannot set attribute with value"
                            " of type `%s', `push_settings' expected" % x.__class__.__name__)

    @property
    def users_count(self):
        if self._users_count is None:
            self._users_count = self._fetch_field('users_count')
        return self._users_count

    @users_count.setter
    def users_count(self, x):
        if test_intp(x):
            self._users_count = x
        else:
            raise TypeError("Message.users_count: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def admin_id(self):
        if self._admin_id is None:
            self._admin_id = self._fetch_field('admin_id')
        return self._admin_id

    @admin_id.setter
    def admin_id(self, x):
        if test_intp(x):
            self._admin_id = x
        else:
            raise TypeError("Message.admin_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def action(self):
        if self._action is None:
            self._action = self._fetch_field('action')
        return self._action

    @action.setter
    def action(self, x):
        if test_action_str(x):
            self._action = x
        else:
            raise TypeError("Message.action: cannot set attribute with value"
                            " of type `%s', `action_str' expected" % x.__class__.__name__)

    @property
    def action_mid(self):
        if self._action_mid is None:
            self._action_mid = self._fetch_field('action_mid')
        return self._action_mid

    @action_mid.setter
    def action_mid(self, x):
        if type(x) is int:
            self._action_mid = x
        else:
            raise TypeError("Message.action_mid: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def action_email(self):
        if self._action_email is None:
            self._action_email = self._fetch_field('action_email')
        return self._action_email

    @action_email.setter
    def action_email(self, x):
        if type(x) is str:
            self._action_email = x
        else:
            raise TypeError("Message.action_email: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def action_text(self):
        if self._action_text is None:
            self._action_text = self._fetch_field('action_text')
        return self._action_text

    @action_text.setter
    def action_text(self, x):
        if type(x) is str:
            self._action_text = x
        else:
            raise TypeError("Message.action_text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Message.photo_50: cannot set attribute with value"
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
            raise TypeError("Message.photo_100: cannot set attribute with value"
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
            raise TypeError("Message.photo_200: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Chat(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'type', 'title', 'admin_id', 'users')
        self.__attrs_required__ = set(['id', 'type', 'title', 'admin_id'])

        super(Chat, self).__init__(**kwargs)

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
            raise TypeError("Chat.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if type(x) is str:
            self._type = x
        else:
            raise TypeError("Chat.type: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Chat.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def admin_id(self):
        if self._admin_id is None:
            self._admin_id = self._fetch_field('admin_id')
        return self._admin_id

    @admin_id.setter
    def admin_id(self, x):
        if test_intp(x):
            self._admin_id = x
        else:
            raise TypeError("Chat.admin_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def users(self):
        if self._users is None:
            self._users = self._fetch_field('users')
        return self._users

    @users.setter
    def users(self, x):
        if test_intp(x):
            self._users = x
        else:
            raise TypeError("Chat.users: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Comment(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'from_id', 'date', 'text', 'reply_to_user',
        'reply_to_comment', 'attachments')
        self.__attrs_required__ = set(['id', 'from_id', 'date', 'text'])

        super(Comment, self).__init__(**kwargs)

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
            raise TypeError("Comment.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def from_id(self):
        if self._from_id is None:
            self._from_id = self._fetch_field('from_id')
        return self._from_id

    @from_id.setter
    def from_id(self, x):
        if test_intp(x):
            self._from_id = x
        else:
            raise TypeError("Comment.from_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

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
            raise TypeError("Comment.date: cannot set attribute with value"
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
            raise TypeError("Comment.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def reply_to_user(self):
        if self._reply_to_user is None:
            self._reply_to_user = self._fetch_field('reply_to_user')
        return self._reply_to_user

    @reply_to_user.setter
    def reply_to_user(self, x):
        if type(x) is int:
            self._reply_to_user = x
        else:
            raise TypeError("Comment.reply_to_user: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def reply_to_comment(self):
        if self._reply_to_comment is None:
            self._reply_to_comment = self._fetch_field('reply_to_comment')
        return self._reply_to_comment

    @reply_to_comment.setter
    def reply_to_comment(self, x):
        if test_intp(x):
            self._reply_to_comment = x
        else:
            raise TypeError("Comment.reply_to_comment: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = self._fetch_field('attachments')
        return self._attachments

    @attachments.setter
    def attachments(self, x):
        if type(x) is Attachment_w:
            self._attachments = x
        else:
            raise TypeError("Comment.attachments: cannot set attribute with value"
                            " of type `%s', `Attachment_w' expected" % x.__class__.__name__)


class Note(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'user_id', 'title', 'text', 'date', 'comments',
        'read_comments', 'view_url')
        self.__attrs_required__ = set(['id', 'user_id', 'title', 'text', 'date'])

        super(Note, self).__init__(**kwargs)

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
            raise TypeError("Note.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def user_id(self):
        if self._user_id is None:
            self._user_id = self._fetch_field('user_id')
        return self._user_id

    @user_id.setter
    def user_id(self, x):
        if test_intp(x):
            self._user_id = x
        else:
            raise TypeError("Note.user_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Note.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Note.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Note.date: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def comments(self):
        if self._comments is None:
            self._comments = self._fetch_field('comments')
        return self._comments

    @comments.setter
    def comments(self, x):
        if test_intp(x):
            self._comments = x
        else:
            raise TypeError("Note.comments: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def read_comments(self):
        if self._read_comments is None:
            self._read_comments = self._fetch_field('read_comments')
        return self._read_comments

    @read_comments.setter
    def read_comments(self, x):
        if type(x) is int:
            self._read_comments = x
        else:
            raise TypeError("Note.read_comments: cannot set attribute with value"
                            " of type `%s', `int' expected" % x.__class__.__name__)

    @property
    def view_url(self):
        if self._view_url is None:
            self._view_url = self._fetch_field('view_url')
        return self._view_url

    @view_url.setter
    def view_url(self, x):
        if type(x) is str:
            self._view_url = x
        else:
            raise TypeError("Note.view_url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Page(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'group_id', 'creator_id', 'title',
        'current_user_can_edit', 'current_user_can_edit_access',
        'who_can_view', 'who_can_edit', 'edited', 'created', 'editor_id',
        'views', 'parent', 'parent2', 'source', 'html', 'view_url')
        self.__attrs_required__ = set(['id', 'group_id', 'creator_id', 'title', 'who_can_view', 'who_can_edit', 'created', 'view_url'])

        super(Page, self).__init__(**kwargs)

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
            raise TypeError("Page.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def group_id(self):
        if self._group_id is None:
            self._group_id = self._fetch_field('group_id')
        return self._group_id

    @group_id.setter
    def group_id(self, x):
        if test_intp(x):
            self._group_id = x
        else:
            raise TypeError("Page.group_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def creator_id(self):
        if self._creator_id is None:
            self._creator_id = self._fetch_field('creator_id')
        return self._creator_id

    @creator_id.setter
    def creator_id(self, x):
        if test_intp(x):
            self._creator_id = x
        else:
            raise TypeError("Page.creator_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Page.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def current_user_can_edit(self):
        if self._current_user_can_edit is None:
            self._current_user_can_edit = self._fetch_field('current_user_can_edit')
        return self._current_user_can_edit

    @current_user_can_edit.setter
    def current_user_can_edit(self, x):
        if test_int1(x):
            self._current_user_can_edit = x
        else:
            raise TypeError("Page.current_user_can_edit: cannot set attribute with value"
                            " of type `%s', `int1' expected" % x.__class__.__name__)

    @property
    def current_user_can_edit_access(self):
        if self._current_user_can_edit_access is None:
            self._current_user_can_edit_access = self._fetch_field('current_user_can_edit_access')
        return self._current_user_can_edit_access

    @current_user_can_edit_access.setter
    def current_user_can_edit_access(self, x):
        if test_int1(x):
            self._current_user_can_edit_access = x
        else:
            raise TypeError("Page.current_user_can_edit_access: cannot set attribute with value"
                            " of type `%s', `int1' expected" % x.__class__.__name__)

    @property
    def who_can_view(self):
        if self._who_can_view is None:
            self._who_can_view = self._fetch_field('who_can_view')
        return self._who_can_view

    @who_can_view.setter
    def who_can_view(self, x):
        if test_int_0_1_2(x):
            self._who_can_view = x
        else:
            raise TypeError("Page.who_can_view: cannot set attribute with value"
                            " of type `%s', `int_0_1_2' expected" % x.__class__.__name__)

    @property
    def who_can_edit(self):
        if self._who_can_edit is None:
            self._who_can_edit = self._fetch_field('who_can_edit')
        return self._who_can_edit

    @who_can_edit.setter
    def who_can_edit(self, x):
        if test_int_0_1_2(x):
            self._who_can_edit = x
        else:
            raise TypeError("Page.who_can_edit: cannot set attribute with value"
                            " of type `%s', `int_0_1_2' expected" % x.__class__.__name__)

    @property
    def edited(self):
        if self._edited is None:
            self._edited = self._fetch_field('edited')
        return self._edited

    @edited.setter
    def edited(self, x):
        if test_intp(x):
            self._edited = x
        else:
            raise TypeError("Page.edited: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def created(self):
        if self._created is None:
            self._created = self._fetch_field('created')
        return self._created

    @created.setter
    def created(self, x):
        if test_intp(x):
            self._created = x
        else:
            raise TypeError("Page.created: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def editor_id(self):
        if self._editor_id is None:
            self._editor_id = self._fetch_field('editor_id')
        return self._editor_id

    @editor_id.setter
    def editor_id(self, x):
        if test_intp(x):
            self._editor_id = x
        else:
            raise TypeError("Page.editor_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def views(self):
        if self._views is None:
            self._views = self._fetch_field('views')
        return self._views

    @views.setter
    def views(self, x):
        if test_intp(x):
            self._views = x
        else:
            raise TypeError("Page.views: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def parent(self):
        if self._parent is None:
            self._parent = self._fetch_field('parent')
        return self._parent

    @parent.setter
    def parent(self, x):
        if type(x) is str:
            self._parent = x
        else:
            raise TypeError("Page.parent: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def parent2(self):
        if self._parent2 is None:
            self._parent2 = self._fetch_field('parent2')
        return self._parent2

    @parent2.setter
    def parent2(self, x):
        if type(x) is str:
            self._parent2 = x
        else:
            raise TypeError("Page.parent2: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def source(self):
        if self._source is None:
            self._source = self._fetch_field('source')
        return self._source

    @source.setter
    def source(self, x):
        if type(x) is str:
            self._source = x
        else:
            raise TypeError("Page.source: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def html(self):
        if self._html is None:
            self._html = self._fetch_field('html')
        return self._html

    @html.setter
    def html(self, x):
        if type(x) is str:
            self._html = x
        else:
            raise TypeError("Page.html: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def view_url(self):
        if self._view_url is None:
            self._view_url = self._fetch_field('view_url')
        return self._view_url

    @view_url.setter
    def view_url(self, x):
        if type(x) is str:
            self._view_url = x
        else:
            raise TypeError("Page.view_url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Attachment_m(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('type', 'photo', 'video', 'audio', 'doc', 'wall',
        'wall_reply')
        self.__attrs_required__ = set(['type'])

        super(Attachment_m, self).__init__(**kwargs)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if test_attach_type(x):
            self._type = x
        else:
            raise TypeError("Attachment_m.type: cannot set attribute with value"
                            " of type `%s', `attach_type' expected" % x.__class__.__name__)

    @property
    def photo(self):
        if self._photo is None:
            self._photo = self._fetch_field('photo')
        return self._photo

    @photo.setter
    def photo(self, x):
        if type(x) is Photo:
            self._photo = x
        else:
            raise TypeError("Attachment_m.photo: cannot set attribute with value"
                            " of type `%s', `Photo' expected" % x.__class__.__name__)

    @property
    def video(self):
        if self._video is None:
            self._video = self._fetch_field('video')
        return self._video

    @video.setter
    def video(self, x):
        if type(x) is Video:
            self._video = x
        else:
            raise TypeError("Attachment_m.video: cannot set attribute with value"
                            " of type `%s', `Video' expected" % x.__class__.__name__)

    @property
    def audio(self):
        if self._audio is None:
            self._audio = self._fetch_field('audio')
        return self._audio

    @audio.setter
    def audio(self, x):
        if type(x) is Audio:
            self._audio = x
        else:
            raise TypeError("Attachment_m.audio: cannot set attribute with value"
                            " of type `%s', `Audio' expected" % x.__class__.__name__)

    @property
    def doc(self):
        if self._doc is None:
            self._doc = self._fetch_field('doc')
        return self._doc

    @doc.setter
    def doc(self, x):
        if type(x) is Document:
            self._doc = x
        else:
            raise TypeError("Attachment_m.doc: cannot set attribute with value"
                            " of type `%s', `Document' expected" % x.__class__.__name__)

    @property
    def wall(self):
        if self._wall is None:
            self._wall = self._fetch_field('wall')
        return self._wall

    @wall.setter
    def wall(self, x):
        if type(x) is Wall:
            self._wall = x
        else:
            raise TypeError("Attachment_m.wall: cannot set attribute with value"
                            " of type `%s', `Wall' expected" % x.__class__.__name__)

    @property
    def wall_reply(self):
        if self._wall_reply is None:
            self._wall_reply = self._fetch_field('wall_reply')
        return self._wall_reply

    @wall_reply.setter
    def wall_reply(self, x):
        if type(x) is WallReply:
            self._wall_reply = x
        else:
            raise TypeError("Attachment_m.wall_reply: cannot set attribute with value"
                            " of type `%s', `WallReply' expected" % x.__class__.__name__)


class Wall(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'to_id', 'from_id', 'date', 'text', 'comments',
        'likes', 'reposts', 'attachments', 'geo', 'post_source', 'signer_id',
        'copy_owner_id', 'copy_post_id', 'copy_text')
        self.__attrs_required__ = set(['id', 'to_id', 'from_id', 'date', 'text'])

        super(Wall, self).__init__(**kwargs)

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
            raise TypeError("Wall.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def to_id(self):
        if self._to_id is None:
            self._to_id = self._fetch_field('to_id')
        return self._to_id

    @to_id.setter
    def to_id(self, x):
        if type(x) is int:
            self._to_id = x
        else:
            raise TypeError("Wall.to_id: cannot set attribute with value"
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
            raise TypeError("Wall.from_id: cannot set attribute with value"
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
            raise TypeError("Wall.date: cannot set attribute with value"
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
            raise TypeError("Wall.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Wall.comments: cannot set attribute with value"
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
            raise TypeError("Wall.likes: cannot set attribute with value"
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
            raise TypeError("Wall.reposts: cannot set attribute with value"
                            " of type `%s', `RepostsInfo' expected" % x.__class__.__name__)

    @property
    def attachments(self):
        if self._attachments is None:
            self._attachments = self._fetch_field('attachments')
        return self._attachments

    @attachments.setter
    def attachments(self, x):
        if type(x) is Attachment_w:
            self._attachments = x
        else:
            raise TypeError("Wall.attachments: cannot set attribute with value"
                            " of type `%s', `Attachment_w' expected" % x.__class__.__name__)

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
            raise TypeError("Wall.geo: cannot set attribute with value"
                            " of type `%s', `Geo' expected" % x.__class__.__name__)

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
            raise TypeError("Wall.post_source: cannot set attribute with value"
                            " of type `%s', `Source' expected" % x.__class__.__name__)

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
            raise TypeError("Wall.signer_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def copy_owner_id(self):
        if self._copy_owner_id is None:
            self._copy_owner_id = self._fetch_field('copy_owner_id')
        return self._copy_owner_id

    @copy_owner_id.setter
    def copy_owner_id(self, x):
        if test_intp(x):
            self._copy_owner_id = x
        else:
            raise TypeError("Wall.copy_owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def copy_post_id(self):
        if self._copy_post_id is None:
            self._copy_post_id = self._fetch_field('copy_post_id')
        return self._copy_post_id

    @copy_post_id.setter
    def copy_post_id(self, x):
        if test_intp(x):
            self._copy_post_id = x
        else:
            raise TypeError("Wall.copy_post_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def copy_text(self):
        if self._copy_text is None:
            self._copy_text = self._fetch_field('copy_text')
        return self._copy_text

    @copy_text.setter
    def copy_text(self, x):
        if type(x) is str:
            self._copy_text = x
        else:
            raise TypeError("Wall.copy_text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class WallReply(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'to_id', 'from_id', 'date', 'text', 'likes',
        'reply_to_uid', 'reply_to_cid')
        self.__attrs_required__ = set(['id', 'to_id', 'from_id', 'date', 'text'])

        super(WallReply, self).__init__(**kwargs)

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
            raise TypeError("WallReply.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def to_id(self):
        if self._to_id is None:
            self._to_id = self._fetch_field('to_id')
        return self._to_id

    @to_id.setter
    def to_id(self, x):
        if type(x) is int:
            self._to_id = x
        else:
            raise TypeError("WallReply.to_id: cannot set attribute with value"
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
            raise TypeError("WallReply.from_id: cannot set attribute with value"
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
            raise TypeError("WallReply.date: cannot set attribute with value"
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
            raise TypeError("WallReply.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("WallReply.likes: cannot set attribute with value"
                            " of type `%s', `LikesInfo' expected" % x.__class__.__name__)

    @property
    def reply_to_uid(self):
        if self._reply_to_uid is None:
            self._reply_to_uid = self._fetch_field('reply_to_uid')
        return self._reply_to_uid

    @reply_to_uid.setter
    def reply_to_uid(self, x):
        if test_intp(x):
            self._reply_to_uid = x
        else:
            raise TypeError("WallReply.reply_to_uid: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def reply_to_cid(self):
        if self._reply_to_cid is None:
            self._reply_to_cid = self._fetch_field('reply_to_cid')
        return self._reply_to_cid

    @reply_to_cid.setter
    def reply_to_cid(self, x):
        if test_intp(x):
            self._reply_to_cid = x
        else:
            raise TypeError("WallReply.reply_to_cid: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Attachment_w(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('type', 'photo', 'posted_photo', 'video', 'audio',
        'doc', 'graffiti', 'link', 'note', 'app', 'poll', 'page', 'album')
        self.__attrs_required__ = set(['type'])

        super(Attachment_w, self).__init__(**kwargs)

    @property
    def type(self):
        if self._type is None:
            self._type = self._fetch_field('type')
        return self._type

    @type.setter
    def type(self, x):
        if test_attach_type(x):
            self._type = x
        else:
            raise TypeError("Attachment_w.type: cannot set attribute with value"
                            " of type `%s', `attach_type' expected" % x.__class__.__name__)

    @property
    def photo(self):
        if self._photo is None:
            self._photo = self._fetch_field('photo')
        return self._photo

    @photo.setter
    def photo(self, x):
        if type(x) is Photo:
            self._photo = x
        else:
            raise TypeError("Attachment_w.photo: cannot set attribute with value"
                            " of type `%s', `Photo' expected" % x.__class__.__name__)

    @property
    def posted_photo(self):
        if self._posted_photo is None:
            self._posted_photo = self._fetch_field('posted_photo')
        return self._posted_photo

    @posted_photo.setter
    def posted_photo(self, x):
        if type(x) is PostedPhoto:
            self._posted_photo = x
        else:
            raise TypeError("Attachment_w.posted_photo: cannot set attribute with value"
                            " of type `%s', `PostedPhoto' expected" % x.__class__.__name__)

    @property
    def video(self):
        if self._video is None:
            self._video = self._fetch_field('video')
        return self._video

    @video.setter
    def video(self, x):
        if type(x) is Video:
            self._video = x
        else:
            raise TypeError("Attachment_w.video: cannot set attribute with value"
                            " of type `%s', `Video' expected" % x.__class__.__name__)

    @property
    def audio(self):
        if self._audio is None:
            self._audio = self._fetch_field('audio')
        return self._audio

    @audio.setter
    def audio(self, x):
        if type(x) is Audio:
            self._audio = x
        else:
            raise TypeError("Attachment_w.audio: cannot set attribute with value"
                            " of type `%s', `Audio' expected" % x.__class__.__name__)

    @property
    def doc(self):
        if self._doc is None:
            self._doc = self._fetch_field('doc')
        return self._doc

    @doc.setter
    def doc(self, x):
        if type(x) is Document:
            self._doc = x
        else:
            raise TypeError("Attachment_w.doc: cannot set attribute with value"
                            " of type `%s', `Document' expected" % x.__class__.__name__)

    @property
    def graffiti(self):
        if self._graffiti is None:
            self._graffiti = self._fetch_field('graffiti')
        return self._graffiti

    @graffiti.setter
    def graffiti(self, x):
        if type(x) is Graffiti:
            self._graffiti = x
        else:
            raise TypeError("Attachment_w.graffiti: cannot set attribute with value"
                            " of type `%s', `Graffiti' expected" % x.__class__.__name__)

    @property
    def link(self):
        if self._link is None:
            self._link = self._fetch_field('link')
        return self._link

    @link.setter
    def link(self, x):
        if type(x) is Link:
            self._link = x
        else:
            raise TypeError("Attachment_w.link: cannot set attribute with value"
                            " of type `%s', `Link' expected" % x.__class__.__name__)

    @property
    def note(self):
        if self._note is None:
            self._note = self._fetch_field('note')
        return self._note

    @note.setter
    def note(self, x):
        if type(x) is Note:
            self._note = x
        else:
            raise TypeError("Attachment_w.note: cannot set attribute with value"
                            " of type `%s', `Note' expected" % x.__class__.__name__)

    @property
    def app(self):
        if self._app is None:
            self._app = self._fetch_field('app')
        return self._app

    @app.setter
    def app(self, x):
        if type(x) is App:
            self._app = x
        else:
            raise TypeError("Attachment_w.app: cannot set attribute with value"
                            " of type `%s', `App' expected" % x.__class__.__name__)

    @property
    def poll(self):
        if self._poll is None:
            self._poll = self._fetch_field('poll')
        return self._poll

    @poll.setter
    def poll(self, x):
        if type(x) is Poll:
            self._poll = x
        else:
            raise TypeError("Attachment_w.poll: cannot set attribute with value"
                            " of type `%s', `Poll' expected" % x.__class__.__name__)

    @property
    def page(self):
        if self._page is None:
            self._page = self._fetch_field('page')
        return self._page

    @page.setter
    def page(self, x):
        if type(x) is Page:
            self._page = x
        else:
            raise TypeError("Attachment_w.page: cannot set attribute with value"
                            " of type `%s', `Page' expected" % x.__class__.__name__)

    @property
    def album(self):
        if self._album is None:
            self._album = self._fetch_field('album')
        return self._album

    @album.setter
    def album(self, x):
        if type(x) is Album:
            self._album = x
        else:
            raise TypeError("Attachment_w.album: cannot set attribute with value"
                            " of type `%s', `Album' expected" % x.__class__.__name__)


class PostedPhoto(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'photo_130', 'photo_604')
        self.__attrs_required__ = set(['id', 'owner_id', 'photo_130', 'photo_604'])

        super(PostedPhoto, self).__init__(**kwargs)

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
            raise TypeError("PostedPhoto.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("PostedPhoto.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def photo_130(self):
        if self._photo_130 is None:
            self._photo_130 = self._fetch_field('photo_130')
        return self._photo_130

    @photo_130.setter
    def photo_130(self, x):
        if type(x) is str:
            self._photo_130 = x
        else:
            raise TypeError("PostedPhoto.photo_130: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_604(self):
        if self._photo_604 is None:
            self._photo_604 = self._fetch_field('photo_604')
        return self._photo_604

    @photo_604.setter
    def photo_604(self, x):
        if type(x) is str:
            self._photo_604 = x
        else:
            raise TypeError("PostedPhoto.photo_604: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Graffiti(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'photo_200', 'photo_586')
        self.__attrs_required__ = set(['id', 'owner_id', 'photo_200', 'photo_586'])

        super(Graffiti, self).__init__(**kwargs)

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
            raise TypeError("Graffiti.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("Graffiti.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

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
            raise TypeError("Graffiti.photo_200: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_586(self):
        if self._photo_586 is None:
            self._photo_586 = self._fetch_field('photo_586')
        return self._photo_586

    @photo_586.setter
    def photo_586(self, x):
        if type(x) is str:
            self._photo_586 = x
        else:
            raise TypeError("Graffiti.photo_586: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Link(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('url', 'title', 'description', 'image_src',
        'preview_page', 'preview_url')
        self.__attrs_required__ = set(['url', 'title'])

        super(Link, self).__init__(**kwargs)

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
            raise TypeError("Link.url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def title(self):
        if self._title is None:
            self._title = self._fetch_field('title')
        return self._title

    @title.setter
    def title(self, x):
        if type(x) is str:
            self._title = x
        else:
            raise TypeError("Link.title: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

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
            raise TypeError("Link.description: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def image_src(self):
        if self._image_src is None:
            self._image_src = self._fetch_field('image_src')
        return self._image_src

    @image_src.setter
    def image_src(self, x):
        if type(x) is str:
            self._image_src = x
        else:
            raise TypeError("Link.image_src: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def preview_page(self):
        if self._preview_page is None:
            self._preview_page = self._fetch_field('preview_page')
        return self._preview_page

    @preview_page.setter
    def preview_page(self, x):
        if type(x) is str:
            self._preview_page = x
        else:
            raise TypeError("Link.preview_page: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def preview_url(self):
        if self._preview_url is None:
            self._preview_url = self._fetch_field('preview_url')
        return self._preview_url

    @preview_url.setter
    def preview_url(self, x):
        if type(x) is str:
            self._preview_url = x
        else:
            raise TypeError("Link.preview_url: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class App(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'photo_130', 'photo_604')
        self.__attrs_required__ = set(['id', 'owner_id', 'photo_130', 'photo_604'])

        super(App, self).__init__(**kwargs)

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
            raise TypeError("App.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("App.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def photo_130(self):
        if self._photo_130 is None:
            self._photo_130 = self._fetch_field('photo_130')
        return self._photo_130

    @photo_130.setter
    def photo_130(self, x):
        if type(x) is str:
            self._photo_130 = x
        else:
            raise TypeError("App.photo_130: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def photo_604(self):
        if self._photo_604 is None:
            self._photo_604 = self._fetch_field('photo_604')
        return self._photo_604

    @photo_604.setter
    def photo_604(self, x):
        if type(x) is str:
            self._photo_604 = x
        else:
            raise TypeError("App.photo_604: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)


class Poll(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'owner_id', 'created', 'question', 'votes',
        'answer_id', 'answers')
        self.__attrs_required__ = set(['id', 'owner_id', 'created', 'question', 'votes'])

        super(Poll, self).__init__(**kwargs)

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
            raise TypeError("Poll.id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._fetch_field('owner_id')
        return self._owner_id

    @owner_id.setter
    def owner_id(self, x):
        if test_intp(x):
            self._owner_id = x
        else:
            raise TypeError("Poll.owner_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def created(self):
        if self._created is None:
            self._created = self._fetch_field('created')
        return self._created

    @created.setter
    def created(self, x):
        if test_intp(x):
            self._created = x
        else:
            raise TypeError("Poll.created: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def question(self):
        if self._question is None:
            self._question = self._fetch_field('question')
        return self._question

    @question.setter
    def question(self, x):
        if type(x) is str:
            self._question = x
        else:
            raise TypeError("Poll.question: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def votes(self):
        if self._votes is None:
            self._votes = self._fetch_field('votes')
        return self._votes

    @votes.setter
    def votes(self, x):
        if test_intp(x):
            self._votes = x
        else:
            raise TypeError("Poll.votes: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def answer_id(self):
        if self._answer_id is None:
            self._answer_id = self._fetch_field('answer_id')
        return self._answer_id

    @answer_id.setter
    def answer_id(self, x):
        if test_intp(x):
            self._answer_id = x
        else:
            raise TypeError("Poll.answer_id: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def answers(self):
        if self._answers is None:
            self._answers = self._fetch_field('answers')
        return self._answers

    @answers.setter
    def answers(self, x):
        if type(x) is Answer:
            self._answers = x
        else:
            raise TypeError("Poll.answers: cannot set attribute with value"
                            " of type `%s', `Answer' expected" % x.__class__.__name__)


class Answer(PlainObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('id', 'text', 'votes', 'rate')
        self.__attrs_required__ = set(['id', 'text', 'votes'])

        super(Answer, self).__init__(**kwargs)

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
            raise TypeError("Answer.id: cannot set attribute with value"
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
            raise TypeError("Answer.text: cannot set attribute with value"
                            " of type `%s', `str' expected" % x.__class__.__name__)

    @property
    def votes(self):
        if self._votes is None:
            self._votes = self._fetch_field('votes')
        return self._votes

    @votes.setter
    def votes(self, x):
        if test_intp(x):
            self._votes = x
        else:
            raise TypeError("Answer.votes: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)

    @property
    def rate(self):
        if self._rate is None:
            self._rate = self._fetch_field('rate')
        return self._rate

    @rate.setter
    def rate(self, x):
        if test_intp(x):
            self._rate = x
        else:
            raise TypeError("Answer.rate: cannot set attribute with value"
                            " of type `%s', `intp' expected" % x.__class__.__name__)


class Privacy(VKObject):

    def __init__(self, **kwargs):
        self.__attrs__ = ('privacy_view')
        self.__attrs_required__ = set()

        super(Privacy, self).__init__(**kwargs)

    @property
    def privacy_view(self):
        if self._privacy_view is None:
            self._privacy_view = self._fetch_field('privacy_view')
        return self._privacy_view

    @privacy_view.setter
    def privacy_view(self, x):
        if test_privacy_view(x):
            self._privacy_view = x
        else:
            raise TypeError("Privacy.privacy_view: cannot set attribute with value"
                            " of type `%s', `privacy_view' expected" % x.__class__.__name__)



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

