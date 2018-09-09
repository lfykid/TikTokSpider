

## 解锁手机抓包技能

1. 确保手机和电脑在同一个局域网
2. Charles里设置 Proxy - Proxy Settings - Http-Proxy, port设置为8888，勾选enable transparent HTTP proxying
3. 在Charles里 Help - SSL proxying -  install charles root certificate on a mobile device or remote
4. 按步骤3的提示在手机连接的wifi上设置   代理 - 手动 - 输入3里要求的IP和端口
5. 使用第三方浏览器访问chls.pro/ssl 下载pem证书，通过 设置---更多设置---系统安全---从存储设备安装--选择文件 进行安装
6. 以上完成后即可正式的对手机进行抓包



#### 成果

随便点开一个抖音视频，观察抓到的网址，通过关键字dy过滤，可以看到视频源地址url为

http://v3-dy-z.ixigua.com/fcbe3c977ce612147e47e6450ae9b60c/5b87abed/video/m/220279cd152b24b4a1d953cab94c6818f18115a9d1d00010a7eaf9e9a44/



先随便试一个视频

通过charles找到视频地址copy as curl，然后粘贴到postman中，获得requests源码，修改一下保存代码，bingo!

```python
import requests

url = "http://v3-dy-y.ixigua.com/7c0a21fa9c4c6108f1482d6b6769ca6c/5b921c99/video/m/2208175becfbb8a40e48ccf94c58df84eff115b57ab000081cb4d8ed0c5/"

headers = {
    'Range':         "bytes=0-10485760",
    'Vpwp-Type':     "preloader",
    'Vpwp-Key':      "683A5AD25479CE507F8D2EC34799A6E6",
    'Vpwp-Raw-Key':  "v0200f5d0000be8koqaepr11885ngtr0720p",
    'Vpwp-Flag':     "0",
    'Host':          "v3-dy-y.ixigua.com",
    'User-Agent':    "okhttp/3.10.0.1",
    'Cache-Control': "no-cache",
    'Postman-Token': "47c1d073-7f67-44b2-8c2e-ee680cfb8966"
}

response = requests.request("GET", url, headers=headers)

with open('dy.mp4', 'wb') as f:
    f.write(response.content)
    f.close()
```

单个视频下载到手。



## 批量爬虫遇到的问题

#### 遇到443了

关charles

#### 遇到重定向问题302

用requests爬虫拒绝301/302页面的重定向而拿到Location(重定向页面URL)

```python
response = requests.request("GET", url, headers=headers, allow_redirects=False)
video_url = response.headers['Location']
```



## 下一步

怎么让爬虫变得更通用呢？

检查参数 

```python
querystring = {
    "user_id":    "68152168500",
    "count":      "21",
    "max_cursor": max_cursor,
    "aid":        "1128",
    "_signature": "9HucchAar.RLDW2U0fv6DPR7nG",
    "dytk":       "14d65256b82dd042058b0eca9f85461b"
}
```

检查发现aid和_signature并不是必须传的，cookie也不是必须，只有dytk必须传，douyintoken? 该如何解密呢？

