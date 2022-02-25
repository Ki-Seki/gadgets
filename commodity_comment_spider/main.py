import os
import random
import time
import re
import requests
import json

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import xlsxwriter

import config

# Options to disable image loading
options = EdgeOptions()
options.use_chromium = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

test_data = {
    '【魅族18s】魅族 18s 8GB+128GB 渡海 5G 骁龙888+ 36W超充 6.2英寸2K曲面屏 6400W高清三摄光学防抖 拍照手机【行情 报价 价格 评测】-京东': [
        (5, '老魅友了，喜欢小屏旗舰机，手感很好，很精致的手机。一见钟情的感觉\n外形外观：精致漂亮\n屏幕音效：好屏幕，好声音\n拍照效果：一般\n运行速度：快\n待机时间：一般\n其他特色：小屏旗舰机'),
        (5, '又回到我大魅族了，以前用过闹特6，感觉还是不错滴，前几天又在这里下了小18s，这手感，这系统，真不戳。感觉这独角兽特别入眼，请原谅大叔一枚竟然喜欢这么少女的颜色???拍照可以，震感十足，手感一流'),
        (5, '18系列轻薄小屏旗舰，手感无敌的存在。小窗功能是众多安卓里最好用的。超声波指纹，震动反馈一如既往优秀。对比18，升级不是很大，感觉就是换了888+。这次买了18S等风色，和18的踏雪对比，感觉还是爱踏雪一丢丢。对比18Pro，就感觉18握持还是要好，小巧，非常讨人喜欢。目前非常难得小屏旗舰。加油魅族，会一直支持的。'),
        (5, '想了好久的小屏旗舰，因为等风颜色太好看了，就买了最高配，正好也省的以后内存不够。我比较喜欢曲面屏，特别是微曲的，而且小屏正好适合手小的我。之前用过mx4一直再等魅族的新品，现在终于有机会再入手啦~目前很满意?'),
        (3, '颜值贼高，发热跟我小米pro好很多，续航嘛我不太在意我又不出远门，偶尔打游戏，我是那种没玩手机就充电的，每天出去电量都是90以上，打游戏嘛，还没适应毕竟小屏嘛我这个大手玩着游戏还没适应哈哈哈，相当满意的哈哈哈'),
        (5, '我在等风，也在等你。8年魅友，这次换机是从16sp过来的，心心念念的18s等风终于到手，这颜值简直绝了，一上手便爱不释手！6.2英寸的机身，162g的轻妙手感，在当今这个旗舰机动不动就半斤的时代，显得格外与众不同，但却深得我心！\n再来说说配置，骁龙888Plus＋旗舰5G处理器，2K屏，120赫兹的刷新率，0.1s超声波指纹解锁，再加上Flyme9.2的加持，该有的都有了，可以说是无可挑剔！使用了几天，这绝佳的手感，这醉人的颜值，这人性化好用且贴心的系统，爱了爱了！\n做为一名老魅友，看到魅族的辉煌不在，心里真是说不出来的滋味，还是那句话：不在你辉煌时慕名而来，也不在你落魄时离你而去。魅族不倒，陪你到老！希望魅族越来越好，走出一天属于自己的小而美的道路！加油，大魅族！'),
        (5, '一直都是双*，一个13mini生活用，一个小米11工作用，小米11太大了，终于找到合适的小屏安卓，屏幕细腻清晰，系统流畅，很是喜欢'),
        (5, '小屏手机无敌，看了很久决定种草1魅族18s，手感无敌，续航比想象中要好，整体系统流畅度在888plus的加持下，没有任何问题，屏幕细腻度在开启2k后十分锐利，观感好，整体手感十分优秀圆润，自己单独买了快充，也比较稳定，比火龙888的温度控制要好。整体还是十分优秀。'),
        (5, '使用了几天才来评价的，壳膜都上了，先说买上绝不后悔，体验verynice，屏幕丝滑，振感优秀，888也没有想象中的烫，非常喜欢flyme的深度定制主题，值得一冲！！！'),
        (5, '魅族18s踏雪这个颜值真的是非常好看，小屏的手感很好不搁手，系统也是很流畅实用，特别是指纹解锁的位置放的太好，解锁速度也是超级快，美中不足的是摄像一般，手机的5g信号不够稳定，希望魅族可以继续带来更好的体验。')
    ],
    'Commodity 2': [
        (2, 'a comment'),
        (3, 'good'),
        (5, 'great')
    ]
}


def get_html(url):
    r = requests.get(url, timeout=30, headers={'user-agent': config.user_agent})
    r.raise_for_status()
    r.encoding = "gbk"
    return r.text


# # Jingdong Spider
# def jd_spider(link):
#     """
#     如果没有任何数据，规定返回 None
#     :param link: Commodity link
#     :return: Commodity's name, rates & comments
#     """
#     data = []
#     driver = Edge(options=options)
#     driver.maximize_window()  # Some buttons can't be clicked if not set this.
#
#     # Set User Agent
#     driver.execute_cdp_cmd('Network.setUserAgentOverride', {
#         "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                      "Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56",
#         "platform": "Windows"})
#     driver.get(link)
#     time.sleep(random.random() * 2 + 2)  # Sleep for [2, 4] seconds.
#
#     # Get commodity name.
#     commodity_name = driver.find_element(By.CSS_SELECTOR, 'div.sku-name').text.strip()
#
#     # Loop of pages.
#     while True:
#         # Get comment items of current web page.
#         comment_items = driver.find_elements(By.CSS_SELECTOR, '.tab-con .comment-item .comment-column.J-comment-column')
#         for item in comment_items:
#             # Get rate.
#             star_elem = item.find_element(By.CSS_SELECTOR, '.comment-star')
#             star = int(star_elem.get_attribute('class')[-1])
#             # Get comment.
#             comment_elem = item.find_element(By.CSS_SELECTOR, '.comment-con')
#             comment = comment_elem.text.replace('<br/>', '\n')
#
#             data.append((star, comment))
#
#         # Break if data is sufficient.
#         if len(data) >= config.max_comments:
#             break
#
#         # Next page
#         try:
#             nextpage = driver.find_element(By.CSS_SELECTOR, '.tab-con a.ui-pager-next')
#
#             # time.sleep(random.random()*2 + 2)  # Sleep for [2, 4] seconds.
#             nextpage.click()
#             # time.sleep(random.random()*2 + 2)  # Sleep for [2, 4] seconds.
#         except NoSuchElementException:
#             break
#
#     driver.close()
#     return commodity_name, data[:config.max_comments]


# Jingdong Spider
def jd_spider(link):
    data = [('Rate', 'Time', 'Content')]
    product_id = re.match(r'(.+)\.html', link).group(1).split('/')[-1]
    # Comments are sorted by time when sortType=6.
    # Page start with 0. So it should start from page=0.
    json_comment_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=6&page={}&pageSize=10'
    for i in range(config.max_comments // 10 + 1):
        json_txt = get_html(json_comment_url.format(product_id, i))[20:-2]
        time.sleep(random.random() * 2 + 2)
        json_obj = json.loads(json_txt)
        comments = json_obj.get('comments', [])
        for comment in comments:
            data.append((comment.get('score', ''), comment.get('creationTime', ''), comment.get('content', '')))
    return data[:config.max_comments]



# Taobao Spider
def taobao_spider(link):
    return []


# 待修改
# Save data to an Excel file.
def save_to_excel(data, filename, worksheet_name):
    # If file already exists, delete it.
    if os.path.exists(filename):
        os.remove(filename)

    # Create a workbook.
    workbook = xlsxwriter.Workbook(filename)
    for key, val in data.items():
        # Rename worksheet with the commodity name.
        worksheet = workbook.add_worksheet(key[:10])

        # Write header.
        worksheet.write('A1', 'RATE')
        worksheet.write('B1', 'COMMENT')

        # Write data.
        for row, (rate, comment) in enumerate(val, start=1):
            worksheet.write(row, 0, rate)
            worksheet.write(row, 1, comment)
    workbook.close()


def main():
    for i, link in enumerate(config.commodity_links):
        data = []
        if 'jd.com' in link:
            data = jd_spider(link)
        elif 'taobao.com' in link:
            data = taobao_spider(link)
        save_to_excel(data, config.filename, f'Commodity {i}')



main()
