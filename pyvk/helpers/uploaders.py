import requests
import random
from pyvk.utils import filter_dict


class _Uploader(object):
    _get_server = _save = _field = _type = _argsmap = None

    def __init__(self, api, **kwargs):
        self._api = api
        self._args = kwargs
        self._server = self._api.call(self._get_server, **self._args)

    def attachments(self, files):
        return ['{_type}{owner_id}_{id}'.format(_type=self._type, **p) for p in files]

    def _upload_common(self, data, **kwargs):

        if data is None:
            uploaded = requests.get(self._server['upload_url'])

        else:
            try:
                field = self._field % 1
            except TypeError:
                field = self._field

            uploaded = requests.post(self._server['upload_url'], files={field: data})
            print(uploaded.json())

        if self._save:
            args = {}
            if self._argsmap:
                for k_args, k_response in self._argsmap.items():
                    args[k_args] = uploaded.json()[k_response]
            else:
                args.update(uploaded.json())
            args.update(kwargs)

            return self._api.call(self._save, **filter_dict(args))
        else:
            return uploaded.json()


class AlbumPhotoUploader(_Uploader):
    _get_server = 'photos.getUploadServer'
    _save = 'photos.save'
    _field = 'file%d'
    _type = 'photo'

    def __init__(self, api, album_id, group_id=None):
        super(AlbumPhotoUploader, self).__init__(api, album_id=album_id, group_id=group_id)

    def upload(self, content, latitude=None, longitude=None, caption=None):
        args = {
            'latitude': latitude,
            'longitude': longitude,
            'caption': caption,
            'album_id': self._args['album_id'],
            'group_id': self._args['group_id'],
        }

        return self._upload_common(('file.jpg', content), **filter_dict(args))


class WallPhotoUploader(_Uploader):
    _get_server = 'photos.getWallUploadServer'
    _save = 'photos.saveWallPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, api, group_id=None):
        super(WallPhotoUploader, self).__init__(api, group_id=group_id)

    def upload(self, content, user_id=None, attach=False):
        photos = self._upload_common(
            ('file.jpg', content), user_id=user_id, group_id=self._args['group_id']
        )
        return self.attachments(photos) if attach else photos


class ProfilePhotoUploader(_Uploader):
    _get_server = 'photos.getOwnerPhotoUploadServer'
    _save = 'photos.saveOwnerPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, api, owner_id=None):
        super(ProfilePhotoUploader, self).__init__(api, owner_id=owner_id)

    def upload(self, content):
        return self._upload_common(('file.jpg', content), owner_id=self._args['owner_id'])


class MessagePhotoUploader(_Uploader):
    _get_server = 'photos.getMessagesUploadServer'
    _save = 'photos.saveMessagesPhoto'
    _field = 'photo'
    _type = 'photo'

    def __init__(self, api):
        super(MessagePhotoUploader, self).__init__(api)

    def upload(self, content, attach=False):
        photos = self._upload_common(('file.jpg', content))
        return self.attachments(photos) if attach else photos


class ChatPhotoUploader(_Uploader):
    _get_server = 'photos.getChatUploadServer'
    _save = 'messages.setChatPhoto'
    photos_per_request = 1
    _field = 'file'
    _type = 'photo'
    _argsmap = {'file': 'response'}

    def __init__(self, api, chat_id, crop_x=None, crop_y=None, crop_width=None):

        super(ChatPhotoUploader, self).__init__(
            api, chat_id=chat_id, crop_x=crop_x, crop_y=crop_y, crop_width=crop_width
        )

    def upload(self, content):
        return self._upload_common(('file.jpg', content))


class MarketPhotoUploader(_Uploader):
    _get_server = 'photos.getMarketUploadServer'
    _save = 'photos.saveMarketPhoto'
    _field = 'file'
    _type = 'photo'

    def __init__(self, api, group_id, main_photo=None, crop_x=None, crop_y=None, crop_width=None):

        super(MarketPhotoUploader, self).__init__(
            api,
            group_id=group_id,
            main_photo=main_photo,
            crop_x=crop_x,
            crop_y=crop_y,
            crop_width=crop_width,
        )

    def upload(self, content):
        return self._upload_common(('file.jpg', content), group_id=self._args['group_id'])


class MarketAlbumPhotoUploader(_Uploader):
    _get_server = 'photos.getMarketAlbumUploadServer'
    _save = 'photos.saveMarketAlbumPhoto'
    _field = 'file'
    _type = 'photo'

    def __init__(self, api, group_id):
        super(MarketAlbumPhotoUploader, self).__init__(api, group_id=group_id)

    def upload(self, content):
        return self._upload_common(('file.jpg', content), group_id=self._args['group_id'])


class AudioUploader(_Uploader):
    _get_server = 'audio.getUploadServer'
    _save = 'audio.save'
    _field = 'file'
    _type = 'audio'

    def __init__(self, api):
        super(AudioUploader, self).__init__(api)

    def upload(self, content, artist=None, title=None):
        name = list('abcdefghijklmnopqr')
        random.shuffle(name)
        return self._upload_common((''.join(name) + '.mp3', content), artist=artist, title=title)


class VideoUploader(_Uploader):
    _get_server = 'video.save'
    _field = 'video_file'
    _type = 'video'

    def __init__(self, api, **kwargs):
        super(VideoUploader, self).__init__(api, **kwargs)

    def upload(self, content=None):
        return self._upload_common(('video', content) if content else None)


class DocUploader(_Uploader):
    _get_server = 'docs.getUploadServer'
    _save = 'docs.save'
    _field = 'file'
    _type = 'doc'

    def __init__(self, api, group_id=None):
        super(DocUploader, self).__init__(api, group_id=group_id)

    def upload(self, filename, content, title=None, tags=None, attach=False):
        files = self._upload_common((filename, content), title=title, tags=tags)
        return self.attachments(files) if attach else files


class DocWallUploader(DocUploader):
    _get_server = 'docs.getWallUploadServer'
