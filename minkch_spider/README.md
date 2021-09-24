# minkch.com 爬虫

## 一 功能

自动爬取 minkch.com 的所有图片视频，并分类保存各数据项到数据库。在 `settings.py` 进行可配置的爬取。

## 二 准备

### 1. 虚拟环境准备

安装：
- 虚拟环境：`pip install virtualenv`
- 虚拟环境管理器：`pip install virtualenvwrapper-win`

一些基本的命令：
- 更改WORKON_HOME：打开控制面板-系统和安全-系统-高级系统设置-环境变量-系统变量-点击新建，变量名：输入 `WORKON_HOME`， 变量值：输入自定义的路径，确定保存，最后**重启**或者**利用 win+r 进入 cmd.exe**即可成功更改目录
- `mkvirtualenv spider`：创建虚拟环境spider
- `workon spider`：进入虚拟环境spider
- `deactivate`：退出虚拟环境
- `rmvirtualenv spider`：移除虚拟环境spider

### 2. 依赖包准备

> - 国内镜像：`pip install -i https://pypi.douban.com/simple python_package_name`
> - 第三方 whl 文件下载提供：[Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

- `pip install lxml` HTML 和 XML 的解析库
- `pip install twisted` 异步框架
- `pip install pywin32` Windows API 库
- `pip install scrapy` Scrapy 框架
- `pip install pillow` Scrapy 图片下载用到的图片处理库
- `pip install mysqlclient` MySQL 数据库连接库

### 3. 数据库准备

```
mysql> desc archives;
+------------------------+-----------+------+-----+---------+-------+
| Field                  | Type      | Null | Key | Default | Extra |
+------------------------+-----------+------+-----+---------+-------+
| id                     | int       | NO   | PRI | NULL    |       |
| title                  | char(100) | NO   |     | NULL    |       |
| title_zh               | char(100) | YES  |     | NULL    |       |
| date_time              | datetime  | YES  |     | NULL    |       |
| tags                   | char(100) | YES  |     | NULL    |       |
| comments               | int       | YES  |     | NULL    |       |
| pre_url                | char(100) | YES  |     | NULL    |       |
| next_url               | char(100) | YES  |     | NULL    |       |
| img_scalar             | tinyint   | YES  |     | NULL    |       |
| video_scalar           | tinyint   | YES  |     | NULL    |       |
| img_got                | tinyint   | YES  |     | NULL    |       |
| video_got              | tinyint   | YES  |     | NULL    |       |
| img_acquisition_rate   | float     | YES  |     | NULL    |       |
| video_acquisition_rate | float     | YES  |     | NULL    |       |
| src_path               | text      | NO   |     | NULL    |       |
+------------------------+-----------+------+-----+---------+-------+
```

### 4. Scrapy 具体使用

1. 在`WORKON_HOME`的目录下，使用`mkvirtualenv env_for_minkch_spider`
2. `workon env_for_minkch_spider`
3. `scrapy startproject MinkchSpider`
4. `cd MinkchSpider`
5. `scrapy genspider minkch minkch.com`
6. 编辑以下源代码即可👇

## 三 源码

> PS. 只展示与Scrapy框架不同的部分

### `MinkchSpider\main.py`

```python
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["execute", "crawl", "minkch"])

```

### `MinkchSpider\MinkchSpider\items.py`

```python
import re

from scrapy.loader import ItemLoader
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join


def id_convert(value):
    match = re.match(r".*/(\d+).html", value)
    if match:
        return match.group(1)
    else:
        print('[My Log] id获取失败，在.\\MinkchSpider\\items.py')


def comments_convert(value):
    match = re.match(r".*?(\d+).*", value)
    if match:
        return match.group(1)
    else:
        print('[My Log] comments获取失败，在.\\MinkchSpider\\items.py')


def fill_link(value):
    return 'https:' + value


class img_scalar_convert:
    def __call__(self, values):
        for value in values:
            match = re.match(r".*?(\d+)枚", value)
            if match:
                return match.group(1)


class video_scalar_convert:
    def __call__(self, values):
        for value in values:
            match = re.match(r".*?(\d+)本", value)
            if match:
                return match.group(1)


class MinkchItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MinkchItem(Item):
    id = Field(
        input_processor=MapCompose(id_convert)
    )
    title = Field()
    title_zh = Field()
    date_time = Field()
    tags = Field(
        output_processor=Join(separator=',')
    )
    comments = Field(
        input_processor=MapCompose(comments_convert)
    )
    pre_url = Field()
    next_url = Field()
    img_scalar = Field(
        output_processor=img_scalar_convert()
    )
    video_scalar = Field(
        output_processor=video_scalar_convert()
    )
    img_urls = Field(
        input_processor=MapCompose(fill_link),
        output_processor=Identity()
    )
    video_urls = Field(
        input_processor=MapCompose(fill_link),
        output_processor=Identity()
    )
    media_urls = Field()
    img_acquisition_rate = Field()
    video_acquisition_rate = Field()
    src_path = Field()

```

### `MinkchSpider\MinkchSpider\pipelines.py`

```python
import re

from scrapy.pipelines.files import FilesPipeline
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor


class MediaPpl(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        # 根据url设置路径 eg. 2020\08\05063857\15965773010.jpg
        match = re.match(r'.*/(\d+/\d+.+)', request.url)
        if match:
            path = match.group(1)[:4] + '/' + match.group(1)[4:6] + '/' + match.group(1)[6:]
            return path
            # scrapy 默认使用‘/’
        else:
            match = re.match(r'https://.*com/(.*)', request.url)
            if match:
                return match.group(1)
            else:
                print('[My Log] filepath定义失败，在.\\MinkchSpider\\pipelines.py')


class MysqlPpl(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        try:
            insert_sql = """
            replace into archives
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = list()
            params.append(item.get('id', 0))
            params.append(item.get('title', ''))
            params.append(item.get('title_zh', ''))
            params.append(item.get('date_time', '1601-01-02 23:59:59'))
            params.append(item.get('tags', ''))
            params.append(item.get('comments', 0))
            params.append(item.get('pre_url', ''))
            params.append(item.get('next_url', ''))
            params.append(item.get('img_scalar', 0))
            params.append(item.get('video_scalar', 0))
            params.append(len(item.get('img_urls', [])))
            params.append(len(item.get('video_urls', [])))
            params.append(item.get('img_acquisition_rate', 0))
            params.append(item.get('video_acquisition_rate', 0))
            params.append(item.get('src_path', ''))
            cursor.execute(insert_sql, tuple(params))
            print('[My Log] Save the data into MySQL Databases: Succeed')
        except:
            print('[My Log] Save the data into MySQL Databases: Fail')

```

### `MinkchSpider\MinkchSpider\settings.py`

```python
import os

BOT_NAME = 'MinkchSpider'

SPIDER_MODULES = ['MinkchSpider.spiders']
NEWSPIDER_MODULE = 'MinkchSpider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure item pipelines
ITEM_PIPELINES = {
   'MinkchSpider.pipelines.MediaPpl': 1,
   'MinkchSpider.pipelines.MysqlPpl': 2,
}

# 爬虫爬取范围
page_range = (200, 250)  # 爬取列表页页码范围，端点值都包括
START_PAGE = page_range[0]  # 爬取的archive列表页的起始页码，每一个列表页包含11篇文章：1个广告，10个archives
ARCHIVE_CRAWL_LIMIT = 10 * (page_range[1]-page_range[0]+1)  # 爬取archive的上限

# 图片和视频的下载开关
DL_IMG = True
DL_VIDEO = True

# 网站基础参数，即archive per page的数量
APP = 10

# 百度翻译API的ID和密钥
BAIDU_APPID = '20200805000533496'
BAIDU_SECRETKEY = 'GNDsrRwMujz3MpFkgwlE'

# 使用scrapy item pipelines要配置的参数
FILES_URLS_FIELD = 'media_urls'
project_dir = os.path.dirname(os.path.abspath(__file__))
FILES_STORE = os.path.join(project_dir, 'medias')

# 数据库相关参数
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'minkch_spider'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'

```

### `MinkchSpider\MinkchSpider\spiders\minkch.py`

```python
import json
import re

import scrapy
from scrapy import Request

from MinkchSpider.items import MinkchItemLoader
from MinkchSpider.items import MinkchItem
from MinkchSpider.utils import common
from MinkchSpider import settings


class MinkchSpider(scrapy.Spider):
    name = 'minkch'
    allowed_domains = ['minkch.com']
    start_urls = ['https://minkch.com/page/{}'.format(settings.START_PAGE)]

    archive_crawl_count = 0  # archive爬取数量计数器

    # 爬取start_url，也即列表开始页的第一条archive的链接并yield给parse_archives
    def parse(self, response):
        first_archive_url = response.xpath('//a[@rel="bookmark" and not(@target="_blank")][1]/@href').extract_first('')
        yield Request(url=first_archive_url, callback=self.parse_archives)

    # 爬取详情页（archive页）
    def parse_archives(self, response):

        # 设置计数器，通过settings.py中的ARCHIVE_CRAWL_LIMIT项来确定爬取archives的上限
        MinkchSpider.archive_crawl_count += 1

        # 日志：打印当前页码和当前archive
        current_page = settings.START_PAGE + MinkchSpider.archive_crawl_count // settings.APP
        current_archive = MinkchSpider.archive_crawl_count % settings.APP
        print('[My Log] Crawling page {}, archive {}'.format(current_page, current_archive))

        # 爬取图片的两种xpath，分别可以解析源图片和网页上显示的图片
        img_xpath = {
            'original': '//div[@class="entry-content clearfix"][last()]//img[@class="pict"]/parent::a/attribute::href',
            'displaying': '//div[@class="entry-content clearfix"][last()]//img[@class="pict"]/attribute::src'}

        # 通过自定义的ItemLoader来解析各项数据到item
        item_loader = MinkchItemLoader(item=MinkchItem(), response=response)
        item_loader.add_value('id', response.url)
        item_loader.add_xpath('title', '//h2[@class="h2 entry-title "]/span/text()')
        item_loader.add_xpath('date_time', '//*[@class="entry-meta-default"]//time/attribute::datetime')
        item_loader.add_xpath('tags', '//div[@class="entry-utility entry-meta"]/a/text()')
        item_loader.add_xpath('comments', '//*[@class="entry-meta-default"]//em/text()')
        item_loader.add_xpath('pre_url', '//*[@id="nav-below"]//a[@rel="prev"]/attribute::href')
        item_loader.add_xpath('next_url', '//*[@id="nav-below"]//a[@rel="next"]/attribute::href')
        item_loader.add_xpath('img_scalar', '//div[@class="entry-content clearfix"][last()]//strong/text()')
        item_loader.add_xpath('video_scalar', '//div[@class="entry-content clearfix"][last()]//strong/text()')
        item_loader.add_xpath('img_urls', img_xpath['original'])
        item_loader.add_xpath('video_urls', '//video//source/attribute::src')
        archive_item = item_loader.load_item()

        # 使用百度翻译api
        yield Request(url=common.get_trans_url(archive_item['title']),
                      meta={'archive_item': archive_item},
                      callback=self.parse_rest,
                      dont_filter=True)

        # 计数比较
        if MinkchSpider.archive_crawl_count < settings.ARCHIVE_CRAWL_LIMIT:
            yield Request(url=archive_item['pre_url'], callback=self.parse_archives)

    # 爬取剩余的：①中文翻译的标题 ②媒体资源汇总 ③资源获取率 ④资源所在文件夹相对路径；并且最终yield item
    def parse_rest(self, response):

        # 中文翻译的标题
        archive_item = response.meta.get('archive_item', '')
        json_data = json.loads(response.text)
        if 'trans_result' in json_data:
            archive_item['title_zh'] = json_data['trans_result'][0]['dst']
        else:
            print('[My Log] 未成功获得翻译结果，在.\\MinkchSpider\\minkch.py')

        # 媒体资源汇总
        archive_item['media_urls'] = []
        if settings.DL_IMG:
            archive_item['media_urls'] += archive_item.get('img_urls', [])
        if settings.DL_VIDEO:
            archive_item['media_urls'] += archive_item.get('video_urls', [])

        # 资源获取率
        if int(archive_item.get('img_scalar', 0)) != 0:
            archive_item['img_acquisition_rate'] = \
                len(archive_item.get('img_urls', [])) / int(archive_item.get('img_scalar', 0))
        else:
            archive_item['img_acquisition_rate'] = 1.0
        if int(archive_item.get('video_scalar', 0)) != 0:
            archive_item['video_acquisition_rate'] = \
                len(archive_item.get('video_urls', [])) / int(archive_item.get('video_scalar', 0))
        else:
            archive_item['video_acquisition_rate'] = 1.0

        # 资源所在文件夹相对路径，相对在MinkchSpider\medias\下，实际即为文件夹名称
        # 资源路径仅作参考，由于网站设计原因，并不准确
        archive_item['src_path'] = ''
        for media_url in archive_item.get('media_urls', ['']):
            match = re.match(r'.*/(\d+)/\d+.+', media_url)
            if match:
                archive_item['src_path'] = \
                    match.group(1)[:4] + '\\' + match.group(1)[4:6] + '\\' + match.group(1)[6:] + '\\'
                break
        if archive_item['src_path'] == '':
            for media_url in archive_item.get('media_urls', ['']):
                match = re.match(r'https://.*com/(.*)', media_url)
                if match:
                    archive_item['src_path'] += match.group(1) + ', '

        yield archive_item

```

### `MinkchSpider\MinkchSpider\utils\common.py`

```python
# common.py contains common functions for minkch project

import hashlib
import urllib.parse
import random

from MinkchSpider import settings


def get_trans_url(q='apple'):
    appid = settings.BAIDU_APPID  # 填写你的appid
    secret_key = settings.BAIDU_SECRETKEY  # 填写你的密钥

    my_url = 'https://api.fanyi.baidu.com/api/trans/vip/translate'

    from_lang = 'auto'  # 原文语种
    to_lang = 'zh'  # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()
    my_url = my_url + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + from_lang + '&to=' + to_lang + \
        '&salt=' + str(salt) + '&sign=' + sign
    return my_url

```