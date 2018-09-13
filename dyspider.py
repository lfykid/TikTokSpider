#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
from argparse import ArgumentParser
from time import sleep

import requests

from head import download_headers, video_headers, Web_UA

VIDEO_URLS, PAGE = [], 1


def get_all_video_urls(user_id, max_cursor, dytk):
    '''
    获取所有视频的源地址
    '''
    url = "https://www.amemv.com/aweme/v1/aweme/post/?"
    params = {'user_id'   : user_id,
              'count'     : 21,
              'max_cursor': max_cursor,
              'dytk'      : dytk}
    try:
        response = requests.request("GET", url, params=params, headers=video_headers)
        if response.status_code == 200:
            data = response.json()
            for li in data['aweme_list']:
                name = li.get('share_info').get('share_desc')
                url = li.get('video').get('play_addr').get('url_list')[0]
                VIDEO_URLS.append([name, url])

            # 下拉获取更多视频
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
            return
    except Exception as e:
        print('failed,', e)
        return


def download_video(index, username, name, url, retry=3):
    '''
     下载视频,显示进度
     '''
    print("\r正在下载第%s个视频: %s" % (index, name))
    try:
        response = requests.get(url, stream=True, headers=download_headers, timeout=15, allow_redirects=False)
        video_url = response.headers['Location']
        video_response = requests.get(video_url, headers=download_headers, timeout=15)

        # 保存视频，显示下载进度
        if video_response.status_code == 200:
            video_size = int(video_response.headers['Content-Length'])
            with open('%s/%s.mp4' % (username, name), 'wb') as f:
                data_length = 0
                for data in video_response.iter_content(chunk_size=1024):
                    data_length += len(data)
                    f.write(data)
                    done = int(50 * data_length / video_size)
                    sys.stdout.write("\r下载进度: [%s%s]" % ('█' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        # 失败重试3次
        elif video_response.status_code != 200 and retry:
            retry -= 1
            download_video(index, username, name, url, retry)
        else:
            return
    except Exception as e:
        print('download failed,', name, e)
        return None


def get_name_and_dytk(num):
    '''
    获取用户名和dytk
    '''
    url = "https://www.amemv.com/share/user/%s" % num
    headers = {'user-agent': Web_UA}
    try:
        response = requests.request("GET", url, headers=headers)
        name = re.findall('<p class="nickname">(.*?)</p>', response.text)[0]
        dytk = re.findall("dytk: '(.*?)'", response.text)[0]
        return name, dytk
    except Exception:
        return


def makedir(name):
    '''
     建立用户名文件夹
     '''
    if not os.path.isdir(name):
        os.mkdir(name)
    else:
        pass


def get_parser():
    '''
    解析参数
    '''
    parser = ArgumentParser()
    parser.add_argument('--uid', dest='user_id', type=int, help='用户的抖音id')
    return parser.parse_args()


def main():
    ''' 主函数 '''
    args = get_parser()
    _id = args.user_id if args.user_id else int(input('请输入你要爬取的抖音用户id: '))
    username, dytk = get_name_and_dytk(_id)
    makedir(username)
    get_all_video_urls(_id, 0, dytk)
    for index, item in enumerate(VIDEO_URLS, 1):
        name = item[0]
        if name == '抖音-原创音乐短视频社区':
            name = name + str(index)
        url = item[1]
        download_video(index, username, name, url)
        sleep(1)


if __name__ == '__main__':
    main()
