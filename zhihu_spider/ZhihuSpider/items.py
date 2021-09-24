# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy

from ZhihuSpider.utils import common
from ZhihuSpider import settings

# 所有的 item 最后都会经过所有的 pipeline，进行处理

class ZhihuQuestionItem(scrapy.Item):
    question_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        """
        :return: 插入 question 表的 sql 语句及参数
        """
        insert_sql = """
        INSERT           
        INTO
            zhihu_question
            (question_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)                       
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """  # 其中 ON DUPLICATE KEY UPDATE 是 MySQL 独有的语句，移库时要注意
        question_id = self["question_id"][0]
        topics = ", ".join(self["topics"])
        url = self["url"][0]
        title = self["title"][0]
        content = self["content"][0] if "content" in self else ""
        answer_num = common.extract_num(self["answer_num"][0])
        comments_num = common.extract_num(self["comments_num"][0])
        watch_user_num = common.extract_num(self["watch_user_num"][0])
        click_num = common.extract_num(self["click_num"][1])
        crawl_time = datetime.datetime.now().strftime(settings.SQL_DATETIME_FORMAT)
        params = \
            (question_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        """
        :return: 插入 answer 表的 sql 语句及参数
        """
        insert_sql = """
        INSERT           
        INTO
            zhihu_answer
            (answer_id, url, question_id, author_id, content, praise_num, comments_num, create_time, update_time, crawl_time)                       
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """  # 其中 ON DUPLICATE KEY UPDATE 是 MySQL 独有的语句，移库时要注意
        params = (self["answer_id"], self["url"], self["question_id"], self["author_id"], self["content"]
                  , self["praise_num"], self["comments_num"],
                  datetime.datetime.fromtimestamp(self["create_time"]).strftime(settings.SQL_DATETIME_FORMAT),
                  datetime.datetime.fromtimestamp(self["update_time"]).strftime(settings.SQL_DATETIME_FORMAT),
                  datetime.datetime.now())
        return insert_sql, params
