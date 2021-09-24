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
