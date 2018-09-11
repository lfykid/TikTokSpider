#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from argparse import ArgumentParser
from time import sleep

import requests
from head import download_headers, video_headers, Web_UA

URL_LIST = []
PAGE = 1


def get_all_video_urls(user_id, max_cursor, dytk):
    global URL_LIST
    url = "https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&count=21&" \
          "max_cursor={}&dytk={}".format(user_id, max_cursor, dytk)
    try:
        response = requests.request("GET", url, headers=video_headers)
        if response.status_code == 200:
            data = response.json()
            for li in data['aweme_list']:
                name = li.get('share_info').get('share_desc')
                url = li.get('video').get('play_addr').get('url_list')[0]
                URL_LIST.append([name, url])
            if data['has_more'] == 1 and data.get('max_cursor') != 0:
                sleep(1)
                global PAGE
                print('正在收集第%s页视频地址' % (PAGE))
                PAGE += 1
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


def get_name_and_dytk(num):
    url = "https://www.amemv.com/share/user/%s" % num
    headers = {'user-agent': Web_UA}
    response = requests.request("GET", url, headers=headers)
    name = re.findall('<p class="nickname">(.*?)</p>', response.text)[0]
    dytk = re.findall("dytk: '(.*?)'", response.text)[0]
    return name, dytk


def makedir(name):
    if not os.path.isdir(name):
        os.mkdir(name)
    else:
        pass


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--uid', dest='user_id', type=int, help='用户的抖音id')
    return parser.parse_args()


def main():
    args = get_parser()
    _id = args.user_id if args.user_id else int(input('请输入你要爬取的抖音用户id: '))
    username, dytk = get_name_and_dytk(_id)
    makedir(username)
    get_all_video_urls(_id, 0, dytk)
    for index, item in enumerate(URL_LIST, 1):
        name = item[0]
        if name == '抖音-原创音乐短视频社区':
            name = name + str(index)
        url = item[1]
        print("正在下载第%s个视频: %s" % (index, name))
        download_video(username, name, url)
        sleep(1)


if __name__ == '__main__':
    main()
