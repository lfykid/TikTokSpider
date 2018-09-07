#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os

import requests

url_list = []

def get_all_video_urls(max_cursor):
    url = "https://www.amemv.com/aweme/v1/aweme/post/"
    querystring = {
        "user_id": "99311023790",
        "count":   "21", "max_cursor": max_cursor,
        "dytk":    "2f6120d834fc42936c8ae5777546f6b5"
    }
    headers = {
        'accept-encoding':  "gzip, deflate, br",
        'accept-language':  "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
        'user-agent':       "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'accept':           "application/json",
        'referer':          "https://www.amemv.com/share/user/99311023790?u_code=md2m918k&timestamp=1536311519&utm_source=qq&utm_campaign=client_share&utm_medium=android&app=aweme&iid=43539176723",
        'authority':        "www.amemv.com",
        'x-requested-with': "XMLHttpRequest",
        'Cache-Control':    "no-cache",
        'Postman-Token':    "a3873c36-c20c-45f3-baf9-d80c6fdae811"
    }
    try:

        global url_list
        response = requests.request("GET", url, headers=headers, params=querystring)
        global url_list
        if response.status_code == 200:
            data = response.json()
            for li in data['aweme_list']:
                name = li.get('share_info').get('share_desc')
                url = li.get('video').get('play_addr').get('url_list')[0]
                url_list.append([name, url])

            if data['has_more'] == 1 and data.get('max_cursor') != 0:
                return get_all_video_urls(data.get('max_cursor'))
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
        headers = {
            'Connection':                "keep-alive",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent':                "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 "
                                         "(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            'Accept':                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*"
                                         "/*;q=0.8",
            'Accept-Encoding':           "gzip, deflate, br",
            'Accept-Language':           "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
            'Cache-Control':             "no-cache",
            'Postman-Token':             "29cf9311-b9cd-4171-afe1-53e6cdabaabf"
        }
        response = requests.request("GET", url, headers=headers, allow_redirects=False)
        video_url = response.headers['Location']

        video_response = requests.get(video_url, headers=headers)
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
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

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
    get_all_video_urls(0)
    for item in url_list:
        name = item[0]
        url = item[1]
        print("正在下载: ", name)
        download_video(username, name, url)

if __name__ == '__main__':
    _id = int(input('输入id: '))
    main(_id)
