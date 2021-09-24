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
