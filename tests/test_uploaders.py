from io import BytesIO
from pyvk import ClientAuth, p_basic, p_market, p_docs
from pyvk.helpers.uploaders import *
from tests.utils import EnvInput
import requests

import pytest


auth = ClientAuth(input=EnvInput, scope=p_basic | p_market | p_docs, disable_cache=True)
auth.auth()
api = auth.api()


def get_random_photo():
    (photo_obj,) = api.photos.get(album_id=237720036, count=1, rev=True)['items']
    photo_url = photo_obj['photo_604']
    return requests.get(photo_url).content


def test_video():
    up = VideoUploader(api, link='https://www.youtube.com/watch?v=dQw4w9WgXcQ', wallpost=True)
    result = up.upload()
    assert 'response' in result


def test_album_photo():
    photo = get_random_photo()
    up = AlbumPhotoUploader(api, album_id=237720036)
    result = up.upload(BytesIO(photo), caption='shakal')
    assert 'jpg' in result[0]['photo_604']


def test_wall_photo():
    photo = get_random_photo()
    up = WallPhotoUploader(api)
    attach = up.upload(BytesIO(photo), attach=True)
    post = api.wall.post(attachments=attach)
    assert post['post_id']


def test_profile_photo():
    (user,) = api.users.get(fields=['photo_max'])
    photo_url = user['photo_max']
    photo = requests.get(photo_url).content

    up = ProfilePhotoUploader(api)
    result = up.upload(BytesIO(photo))
    assert 'photo_src' in result


@pytest.mark.skip()
def test_chat_photo():
    photo = get_random_photo()

    up = ChatPhotoUploader(api, chat_id=1)
    result = up.upload(BytesIO(photo))
    assert 'message_id' in result


@pytest.mark.skip()
def test_message_photo():
    photo = get_random_photo()
    up = MessagePhotoUploader(api)
    attach = up.upload(BytesIO(photo), attach=True)
    msg_id = api.messages.send(chat_id=1, attachment=attach)
    assert type(msg_id) is int


def test_audio():
    (item,) = api.audio.get(count=1)['items']
    audio_url = item['url']
    audio = requests.get(audio_url).content

    up = AudioUploader(api)
    result = up.upload(audio, artist='mr.skletal', title='thanks')
    assert 'id' in result


def test_doc():
    (item,) = api.docs.get(count=1)['items']
    doc_url, doc_name = item['url'], item['title']
    doc = requests.get(doc_url).content

    up = DocUploader(api)
    result = up.upload(doc_name, doc)

    assert type(result) is list
    assert 'id' in result[0]


@pytest.mark.skip()
def test_product_photo():
    (item,) = api.market.getById(item_ids=['-131241381_360858'], extended=True)['items']
    (photo_obj,) = item['photos']
    photo_url = photo_obj['photo_2560']
    photo = requests.get(photo_url).content

    up = MarketPhotoUploader(api, group_id=131241381, main_photo=True)
    result = up.upload(photo)

    assert type(result) is list
    assert 'id' in result[0]


def test_product_collection_photo():
    (item,) = api.market.getById(item_ids=['-131241381_360858'], extended=True)['items']
    (photo_obj,) = item['photos']
    photo_url = photo_obj['photo_2560']
    photo = requests.get(photo_url).content

    up = MarketAlbumPhotoUploader(api, group_id=131241381)
    result = up.upload(photo)

    assert type(result) is list
    assert 'id' in result[0]
