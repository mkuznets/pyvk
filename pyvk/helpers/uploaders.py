import requests
from pyvk.utils import filter_dict


class _Uploader:
    _get_server = _save = _field = _type = None

    def __init__(self, handler, **kwargs):
        self._handler = handler
        self._args = filter_dict(kwargs)
        self._server = self._handler.call(self._get_server, **self._args)

    def attachments(self, files):
        return ['{_type}{owner_id}_{id}'.format(_type=self._type, **p)
                for p in files]

    def _upload_common(self, buffer, **kwargs):

        if buffer is None:
            uploaded = requests.get(self._server['upload_url'])

        else:
            try:
                field = self._field % 1
            except TypeError:
                field = self._field

            uploaded = requests.post(self._server['upload_url'],
                                     files={field: buffer})

        if self._save:
            args = {}
            args.update(uploaded.json())
            args.update(kwargs)

            return self._handler.call(self._save, **filter_dict(args))
        else:
            return uploaded.json()


class AlbumPhotoUploader(_Uploader):
    _get_server = 'photos.getUploadServer'
    _save = 'photos.save'
    _field = 'file%d'
    _type = 'photo'

    def __init__(self, handler, album_id, group_id=None):
        super(AlbumPhotoUploader, self).__init__(
            handler, album_id=album_id, group_id=group_id
        )

    def upload(self, buffer, latitude=None, longitude=None, caption=None):
        args = {'latitude': latitude, 'longitude': longitude,
                'caption': caption, 'album_id': self._args['album_id'],
                'group_id': self._args['group_id']}

        return self._upload_common(buffer, **args)


class WallPhotoUploader(_Uploader):
    _get_server = 'photos.getWallUploadServer'
    _save = 'photos.saveWallPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, handler, group_id=None):
        super(WallPhotoUploader, self).__init__(
            handler, group_id=group_id
        )

    def upload(self, buffer, user_id=None, attach=False):
        photos= self._upload_common(buffer, user_id=user_id,
                                    group_id=self._args['group_id'])
        return self.attachments(photos) if attach else photos


class ProfilePhotoUploader(_Uploader):
    _get_server = 'photos.getOwnerPhotoUploadServer'
    _save = 'photos.saveOwnerPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, handler, owner_id=None):
        super(ProfilePhotoUploader, self).__init__(
            handler, owner_id=owner_id
        )

    def upload(self, buffer):
        return self._upload_common(buffer, owner_id=self._args['owner_id'])


class MessagePhotoUploader(_Uploader):
    _get_server = 'photos.getMessagesUploadServer'
    _save = 'photos.saveMessagesPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, handler):
        super(MessagePhotoUploader, self).__init__(handler)

    def upload(self, buffer, attach=False):
        photos = self._upload_common(buffer)
        return self.attachments(photos) if attach else photos


class ChatPhotoUploader(_Uploader):
    _get_server = 'photos.getChatUploadServer'
    _save = 'messages.setChatPhoto'
    photos_per_request = 1
    _field = 'file'
    _type = 'photo'

    def __init__(self, handler, chat_id,
                 crop_x=None, crop_y=None, crop_width=None):

        super(ChatPhotoUploader, self).__init__(
            handler, chat_id=chat_id, crop_x=crop_x, crop_y=crop_y,
            crop_width=crop_width
        )

    def upload(self, buffer):
        return self._upload_common(buffer)


class MarketPhotoUploader(_Uploader):
    _get_server = 'photos.getMarketUploadServer'
    _save = 'photos.saveMarketPhoto'
    _field = 'file'
    _type = 'photo'

    def __init__(self, handler, group_id, main_photo=None,
                 crop_x=None, crop_y=None, crop_width=None):

        super(MarketPhotoUploader, self).__init__(
            handler, group_id=group_id, main_photo=main_photo,
            crop_x=crop_x, crop_y=crop_y, crop_width=crop_width
        )

    def upload(self, buffer):
        return self._upload_common(buffer, group_id=self._args['group_id'])


class MarketAlbumPhotoUploader(_Uploader):
    _get_server = 'photos.getMarketAlbumUploadServer'
    _save = 'photos.saveMarketAlbumPhoto'
    _field = 'file'
    _type = 'photo'

    def __init__(self, handler, group_id):
        super(MarketAlbumPhotoUploader, self).__init__(
            handler, group_id=group_id
        )

    def upload(self, buffer):
        return self._upload_common(buffer, group_id=self._args['group_id'])


class AudioUploader(_Uploader):
    _get_server = 'audio.getUploadServer'
    _save = 'audio.save'
    _field = 'file'
    _type = 'audio'

    def __init__(self, handler):
        super(AudioUploader, self).__init__(handler)

    def upload(self, buffer, artist=None, title=None):
        return self._upload_common(buffer, artist=artist, title=title)


class VideoUploader(_Uploader):
    _get_server = 'video.save'
    _field = 'video_file'
    _type = 'video'

    def __init__(self, handler, **kwargs):
        super(VideoUploader, self).__init__(handler, **kwargs)

    def upload(self, buffer=None):
        return self._upload_common(buffer)


class DocUploader(_Uploader):
    _get_server = 'docs.getUploadServer'
    _save = 'docs.save'
    _field = 'file'
    _type = 'doc'

    def __init__(self, handler, group_id=None):
        super(DocUploader, self).__init__(handler, group_id=group_id)

    def upload(self, buffer, title=None, tags=None, attach=False):
        files = self._upload_common(buffer, title=title, tags=tags)
        return self.attachments(files) if attach else files


class DocWallUploader(DocUploader):
    _get_server = 'docs.getWallUploadServer'
