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
page_range = (1, 999999)  # 爬取列表页页码范围，端点值都包括
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
