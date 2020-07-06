from io import BytesIO

import pytest

from pyvk.helpers.uploaders import *


def get_random_photo(api):
    (photo_obj,) = api.photos.get(album_id=237720036, count=1, rev=True)['items']
    photo_url = photo_obj['photo_604']
    return requests.get(photo_url).content


@pytest.mark.network
def test_video(api):
    up = VideoUploader(api, link='https://www.youtube.com/watch?v=dQw4w9WgXcQ', wallpost=True)
    result = up.upload()
    assert 'response' in result


@pytest.mark.network
def test_album_photo(api):
    photo = get_random_photo(api)
    up = AlbumPhotoUploader(api, album_id=237720036)
    result = up.upload(BytesIO(photo), caption='shakal')
    assert 'jpg' in result[0]['photo_604']


@pytest.mark.network
def test_wall_photo(api):
    photo = get_random_photo(api)
    up = WallPhotoUploader(api)
    attach = up.upload(BytesIO(photo), attach=True)
    post = api.wall.post(attachments=attach)
    assert post['post_id']


@pytest.mark.network
def test_profile_photo(api):
    (user,) = api.users.get(fields=['photo_max'])
    photo_url = user['photo_max']
    photo = requests.get(photo_url).content

    up = ProfilePhotoUploader(api)
    result = up.upload(BytesIO(photo))
    assert 'photo_src' in result


@pytest.mark.network
@pytest.mark.skip()
def test_chat_photo(api):
    photo = get_random_photo(api)

    up = ChatPhotoUploader(api, chat_id=1)
    result = up.upload(BytesIO(photo))
    assert 'message_id' in result


@pytest.mark.network
@pytest.mark.skip()
def test_message_photo(api):
    photo = get_random_photo(api)
    up = MessagePhotoUploader(api)
    attach = up.upload(BytesIO(photo), attach=True)
    msg_id = api.messages.send(chat_id=1, attachment=attach)
    assert type(msg_id) is int


@pytest.mark.network
def test_audio(api):
    (item,) = api.audio.get(count=1)['items']
    audio_url = item['url']
    audio = requests.get(audio_url).content

    up = AudioUploader(api)
    result = up.upload(audio, artist='mr.skletal', title='thanks')
    assert 'id' in result


@pytest.mark.network
def test_doc(api):
    (item,) = api.docs.get(count=1)['items']
    doc_url, doc_name = item['url'], item['title']
    doc = requests.get(doc_url).content

    up = DocUploader(api)
    result = up.upload(doc_name, doc)

    assert type(result) is list
    assert 'id' in result[0]


@pytest.mark.network
@pytest.mark.skip()
def test_product_photo(api):
    (item,) = api.market.getById(item_ids=['-131241381_360858'], extended=True)['items']
    (photo_obj,) = item['photos']
    photo_url = photo_obj['photo_2560']
    photo = requests.get(photo_url).content

    up = MarketPhotoUploader(api, group_id=131241381, main_photo=True)
    result = up.upload(photo)

    assert type(result) is list
    assert 'id' in result[0]


@pytest.mark.network
def test_product_collection_photo(api):
    (item,) = api.market.getById(item_ids=['-131241381_360858'], extended=True)['items']
    (photo_obj,) = item['photos']
    photo_url = photo_obj['photo_2560']
    photo = requests.get(photo_url).content

    up = MarketAlbumPhotoUploader(api, group_id=131241381)
    result = up.upload(photo)

    assert type(result) is list
    assert 'id' in result[0]
