import praw                     #Импорт библиотек
import urllib.request
import os
import vk
import requests
import json
import time

k = 0
info = {'Post': ' ', 'Title': ' ', 'Img': ' '}
mas = []
reddit = praw.Reddit(client_id='CWh841LZZ28nFQ',                        #Данные для входа в акк-т reddit
                     client_secret='tDSpdxAB6Cw1CT1fKS4cJYuqV-k',
                     password='Varlam30',
                     user_agent='VKBot0.1',
                     username='Exstez')

# print(reddit.user.me())       #Проверка данных на правильность. Если все ок - выводится твой ник с реддита.

reddit.read_only = False        #Отключает ридонли мод ( нужна рабочая авторизация )
#reddit.read_only = True        #Включает ридонли мод

subreddit = reddit.subreddit('battlestations')      #Сабреддита
hot_subreddit = subreddit.hot(limit=25)              #Пункт сабреддита и лимит новостей, top/hot/new/rising

writer = open('post.txt', 'w')                      #Ф-ия записи в файл
for submission in hot_subreddit:                    #Парсер
    mas.append(submission.url)
    if not submission.stickied:
        print('"Пост": http://reddit.com/r/battlestations/comments/{}, "Тайтл": {}, "Картинка": {}'.format(submission,
                                                                                                     submission.title,
                                                                                                     submission.url))
        writer.write(submission.url+'\n')
writer.close()  #Закрыл ф-ию записи в файл
print(mas)

for i in range(1,25): #Лимит новостей
    url = mas[i]
    img = urllib.request.urlopen(url).read()
    out = open("upload\img{}.jpg".format(i), "wb")
    out.write(img)
    out.close

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


time_post = int('1561636800') # Время первой публикации в формате unix timestamp
files = os.listdir(UP_DIR)
for file in files:
    poster = wall_post(file, time_post)
    files.remove(file)
    time.sleep(1)
    time_post += 2 * 60 * 60 # Интервал для публикации записей в секундах
