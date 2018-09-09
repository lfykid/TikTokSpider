#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import os
import requests

from head import download_headers, video_headers, Web_UA

URL_LIST = []

def get_all_video_urls(user_id, max_cursor, dytk):
    global URL_LIST
    url = "https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&count=21&" \
          "max_cursor={}&dytk={}".format(user_id, max_cursor, dytk)  # 此处dytk需要自己替换，还没有破解成功
    try:
        response = requests.request("GET", url, headers=video_headers)
        if response.status_code == 200:
            data = response.json()
            for li in data['aweme_list']:
                name = li.get('share_info').get('share_desc')
                url = li.get('video').get('play_addr').get('url_list')[0]
                URL_LIST.append([name, url])
            if data['has_more'] == 1 and data.get('max_cursor') != 0:
                return get_all_video_urls(user_id, data.get('max_cursor'), dytk)
            else:
                return
        else:
            print(response.status_code)
            return None
    except Exception as e:
        print('failed,', e)
        return None

def download_video(username, name, url):
    try:
        response = requests.request("GET", url, headers=download_headers, allow_redirects=False)
        video_url = response.headers['Location']
        video_response = requests.get(video_url, headers=download_headers)
        video_data = video_response.content
        save_video(username, name, video_data)
    except Exception as e:
        print('download failed,', e)
        return None

def save_video(username, name, data):
    if data:
        with open('%s/%s.mp4' % (username, name), 'wb') as f:
            f.write(data)
            f.close()
    else:
        return

def get_name(num):
    url = "https://www.amemv.com/share/user/%s" % num
    headers = {'user-agent': Web_UA}
    response = requests.request("GET", url, headers=headers)
    name = re.findall('<p class="nickname">(.*?)</p>', response.text)[0]
    return name

def makedir(name):
    if not os.path.isdir(name):
        os.mkdir(name)
    else:
        pass

def main(_id):
    username = get_name(_id)
    makedir(username)
    get_all_video_urls(_id, 0, dytk)
    for item in URL_LIST:
        name = item[0]
        url = item[1]
        print("正在下载: ", name)
        download_video(username, name, url)

if __name__ == '__main__':
    _id = int(input('输入id: '))
    dytk = input('请输入抓到的dytk: ')
    main(_id)
