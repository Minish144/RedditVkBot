import os
import vk
import requests
import json
import time


UP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
group_id = '-183468580' #ID группы со знаком минус в начале
vkapi = vk.OAuthAPI(app_id='7021848', user_login='+79653538013', user_password='Varlam1848130301',
                    scope='offline,photos,wall,groups') # ID Standalone приложения, логин и пароль вк


def wall_post(filename, time_post):
    img = {'photo': (filename, open(UP_DIR + '\\' + filename, 'rb'))}
    up_srv = vkapi.photos.getWallUploadServer(group_id=group_id[1:])
    up_file = requests.post(up_srv['upload_url'], files=img)
    result = json.loads(up_file.text)
    save_file = vkapi.photos.saveWallPhoto(server=result['server'], photo=result['photo'], hash=result['hash'],
                                           group_id=group_id[1:])
    attachments = 'photo' + str(save_file[0]['owner_id']) + '_' + str(save_file[0]['id'])
    post = vkapi.wall.post(owner_id=group_id, from_group='1', attachments=attachments, publish_date=time_post)
    return post


time_post = int('1560693230') # Время первой публикации в формате unix timestamp
files = os.listdir(UP_DIR)
for file in files:
    poster = wall_post(file, time_post)
    files.remove(file)
    time.sleep(1)
    time_post += 1 * 60 * 60 # Интервал для публикации записей. В данном случае 3 часа
