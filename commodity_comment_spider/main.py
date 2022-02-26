import random
import time
import re
import requests
import json

import xlsxwriter
from fake_useragent import UserAgent

import config


def get_html(url, encoding='utf-8'):
    r = requests.get(url, timeout=30, headers={'user-agent': UserAgent().random})
    r.raise_for_status()
    r.encoding = encoding
    return r.text


def jd_spider(link):
    """
    Get the latest comments of a Jingdong commodity from its link.
    :param link: Jingdong commodity's link.
    :return: Scraped data with maximum volume being config.max_comments.
    """
    data = [('Rate', 'Time', 'Content')]
    product_id = re.match(r'(.+)\.html', link).group(1).split('/')[-1]

    # Comments are sorted by time when sortType=6.
    # Page start with 0. So it should start from page=0.
    json_comment_api = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=6&page={}&pageSize=10'

    for page in range(config.max_comments // 10 + 1):
        json_txt = ''
        try:
            url = json_comment_api.format(product_id, page)
            json_txt = get_html(url, 'gbk')[20:-2]
            assert json_txt != ''
        except (requests.exceptions.HTTPError, AssertionError):
            print(f'[ERROR]    Cannot get data of product whose ID is {product_id}')
        time.sleep(random.random() * config.interval + config.interval)
        json_obj = json.loads(json_txt)
        comments = json_obj.get('comments', [])
        if not comments:
            break
        for comment in comments:
            data.append((comment.get('score', ''), comment.get('creationTime', ''), comment.get('content', '')))
    return data[:config.max_comments]


# Taobao Spider
def taobao_spider(link):
    return []


def save_to_excel(data, filename, worksheets):
    """
    Save data to a new Excel file.
    :param data: 3-dimensional (l×m×n) data indicating l worksheets, each of which contains an m×n table.
    :param filename: Name of the Excel file.
    :param worksheets: A string-list consists of worksheets' names.
    """
    workbook = xlsxwriter.Workbook(filename)
    for i, item in enumerate(data):
        worksheet = workbook.add_worksheet(worksheets[i])
        for row, row_data in enumerate(item):
            for col, col_data in enumerate(row_data):
                worksheet.write(row, col, col_data)
    workbook.close()


data = []
for i, (commodity, link) in enumerate(config.commodity_links.items()):
    print(f'\n[PROGRESS] ({i + 1}/{len(config.commodity_links)}) Begin to scrape comments of {commodity}.')
    print(f'           Link: {link}')
    part = []
    if 'jd.com' in link:
        part = jd_spider(link)
    elif 'taobao.com' in link:
        part = taobao_spider(link)
    else:
        print(f'[WARNING]  Program cannot process this link for now.')
    print(f'[NORMAL]   Successfully scraped data.' if part != [] else f'[WARNING]  Failed to scrape data.')
    data.append(part)
save_to_excel(data, config.filename, list(config.commodity_links.keys()))
print(f'[NORMAL]   Successfully saved data to {config.filename}.')
