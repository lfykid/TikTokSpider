![logo](https://github.com/huangke19/TikTokSpider/raw/master/pics/logo.jpg)



# TikTokSpider

![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

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

![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

#### 先随便试一个视频

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



![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

# 抓取指定用户视频

从用户主页的分享页面入手

1. 进入用户主页，点击 - 分享名片 - 链接形式，将主页分享链接发送到电脑上用chrome打开，就可以看到用户的主页面了

   ![dd](https://github.com/huangke19/TikTokSpider/raw/master/pics/Screenshot.png)

2. 但此时还看不到用户的作品，将chrome设置成手机模式，刷新，bingo! 作品出来了

   ![dd](https://github.com/huangke19/TikTokSpider/raw/master/pics/pc.png)

3. 点击作品，下拉，查看network，就可以看到我们要找的作品url列表啦

   ```
   https://www.amemv.com/aweme/v1/aweme/post/?user_id=6xx1xx0&count=21&max_cursor=0&aid=1128&_signature=TG2uvBAbGAHzG19a.rniF0xtrq&dytk=14d65256b82dd042058b0eca9f85461b
   ```

4. 观察一下，这是一个ajax链接，我们需要的所有信息都在返回的包里了

5. 模拟请求，直接点击链接，copy as curl，然后复制到Postman里转成requests代码

6. 返回json里有一个has_more字段，如果为1表示还可以下拉出现更多作品，如果为0表示已经是最后

7. 当我们下拉的时候可以发现，新出现的url里只有max_cursor变了，新出现的max_cursor就是上次请求返回的max_cursor，有了has_more和max_cursor两个参数，我们就可以把所有urls取到了

8. 写一个递归函数 get_all_video_urls 根据has_more字段将所有urls递归爬取下来，终止条件是has_more==0

9. 用一个全局变量url_list = [] 存放爬到的每一个视频的名字和地址

10. 运行编写好的代码后发现，视频数据格式不对，返回去检查，原来第9步中的url不是真实的视频url，而是一个302跳转地址，真实视频地址在第9步response headers里的Location里

11. 添加禁止跳转的代码，获取真实视频url

    ```python
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    video_url = response.headers['Location']
    ```



#### 搞定收工！



![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

## 解决问题

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



## 使用

本代码尚未完善，如果使用，请自行输入要爬用户的id和抓包到的对应dytk参数