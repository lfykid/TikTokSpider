#!/usr/bin/python
# -*- coding: utf-8 -*-

'''把headers单独放到一个文件'''

Web_UA = '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"'

# 爬取所有视频链接url时的headers
video_headers = {
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
# 最终下载视频文件时用的headers
download_headers = {
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
