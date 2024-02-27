![logo](https://github.com/lfykid/TikTokSpider/raw/master/pics/logo.jpg)

# TikTokSpider
## 使用方法

1. 运行dyspider.py文件，输入要爬用户的id  (注意不是手机端的抖音号)

   ![dd](https://github.com/lfykid/TikTokSpider/raw/master/pics/desc.png)

2. 使用命令行参数 --uid 输入用户id

   ```shell
   python dyspider.py --uid 64742778880
   ```

- 抖音号不是抖音ID,UID 获取方式如下：
- 通过 博主Link 获取 sid,/user/后面那一串是SID

```
https://www.douyin.com/user/MS4wLjABAAAA31SF3HKqfHzU-3rfw-FgGqXJ2IsVqpKg_zUSx7hZXfI
```

- 复制sid,替换连接中红色的sid， 打开链接获取 uid
https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=此处填写SID

- 在结果中搜索 UID 即可找到。

## 下载效果

运行代码将会在项目文件夹下新建一个与目标用户同名的文件夹，所有视频皆存入于此

![dd](https://github.com/lfykid/TikTokSpider/raw/master/pics/video.png)

![dd](https://github.com/lfykid/LagouSpider/raw/master/lines/bird.jpg)

## 分析过程

从用户主页的分享页面入手

1. 进入用户主页，点击 - 分享名片 - 链接形式，将主页分享链接发送到电脑上用chrome打开，就可以看到用户的主页面了

   ![dd](https://github.com/lfykid/TikTokSpider/raw/master/pics/Screenshot.png)

2. 但此时还看不到用户的作品，将chrome设置成手机模式，刷新，bingo! 作品出来了

   ![dd](https://github.com/lfykid/TikTokSpider/raw/master/pics/pc.png)

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



2018/09/11更新：添加显示下载进度条功能 



todolist:

- [x] 异常处理
- [ ] 日志功能
- [x] 显示下载进度条