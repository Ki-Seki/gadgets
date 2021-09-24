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
