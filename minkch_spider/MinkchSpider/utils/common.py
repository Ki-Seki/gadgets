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
