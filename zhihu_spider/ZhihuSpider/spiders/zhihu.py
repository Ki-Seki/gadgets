"""
启动此 spider 前需要手动启动 Chrome，cmd 命令如下：
cd 进入 Chrome 可执行文件 所在的目录
执行：chrome.exe --remote-debugging-port=9222
此时在浏览器窗口地址栏访问：http://127.0.0.1:9222/json，如果页面出现 json 数据，则表明手动启动成功

启动此 spider 后，注意与命令行交互！

在 settings 当中要做的：
# ROBOTSTXT_OBEY = False  # 如果不关闭，parse 方法无法执行
# COOKIES_ENABLED = True  # 以便 Request 值在传递时自动传递 cookies
# USER_AGENT = 一个合适的值
# DOWNLOADER_MIDDLEWARES 配置好以备 user agent 的自动变换

"""
import re
import json
import datetime

import scrapy
from scrapy.loader import ItemLoader
from urllib import parse

from ZhihuSpider.utils.browsezhihu import get_cookies
from ZhihuSpider import settings
from ZhihuSpider.items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    # 通用的 question 第一页 answer 请求 url
    # 0: question id, 1: offset, 2: limit
    start_answer_urls = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled&offset={1}&limit={2}&sort_by=default&platform=desktop'

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": settings.USER_AGENT
    }

    # 提取主页所有指向问题的 url
    def parse(self, response, **kwargs):
        # .extract() 是 parsel.selection 中的函数，用于提取元素集合中的 data 域的值
        all_urls = response.css("a::attr(href)").extract()
        # urllib.parse.urljoin 可以合并两个不完整 url
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # (/|$) 表示匹配 / 或“结束”
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:  # 如果是一个含有指向 question 页的 url
                question_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(question_url, callback=self.parse_question, headers=self.headers
                                     , meta={"question_id": question_id, "url": question_url})  # meta 可以向下传递

    def parse_question(self, response):
        """
        提取问题页 question item
        """
        # 使用 ItemLoader 时，每个字段值都是一个 list
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)

        item_loader.add_value("question_id", response.meta.get("question_id", 0))  # 使用 meta 来加载
        item_loader.add_css("topics", "head > meta[name=keywords]::attr(content)")
        item_loader.add_value("url", response.meta.get("url", ''))
        item_loader.add_css("title", "h1.QuestionHeader-title::text")
        item_loader.add_css("content", ".QuestionRichText span:nth-child(1)::text")
        item_loader.add_css("answer_num", ".List-headerText > span::text, .ViewAll:nth-child(1) > a::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::attr(title)")
        item_loader.add_css("click_num", ".NumberBoard-itemValue::attr(title)")

        # 关于获取 create_time update_time
        # request log url of question，接着，将以上 item_loader 的内容改为 meta 字典向下传递
        # 最终交到 get_create_update_of_question 中去打包 question_item 然后 yield
        # 未完成的部分实现如下

        # tmp = response.css(".QuestionHeader-menu > a").extract()[0]
        # log_url = parse.urljoin(self.start_urls[0], tmp)
        # yield scrapy.Request(log_url, callback=self.get_create_update_of_question, headers=self.headers, meta=......)

        question_item = item_loader.load_item()
        yield question_item

        yield scrapy.Request(self.start_answer_urls.format(response.meta.get("question_id", ''), 0, 20)
                             , callback=self.parse_answer, headers=self.headers)

    # def get_create_update_of_question(self, response):
    #     pass

    def parse_answer(self, response):
        """
        提取答案页 answer item
        """
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        next_url = answer_json["paging"]["next"]

        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()

            answer_item["answer_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"]
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, callback=self.parse_answer, headers=self.headers)

    def start_requests(self):
        # 在使用 selenium 前要用以下 cmd 启动 chrome
        # cd "C:\Program Files\Google\Chrome\Application"
        # chrome.exe --remote-debugging-port=9222

        # 不能使用下面的 python 代码的原因是：这个命令是要求返回值的，除非使用多线程
        # os.system('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
        cookies = get_cookies()
        yield scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookies)
