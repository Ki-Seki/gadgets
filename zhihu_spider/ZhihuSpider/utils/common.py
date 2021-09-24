import re


def extract_num(text: str):
    """
    :param text: 字符串文本
    :return: 字符串 text 中的第一次出现的数字；若没有返回 -1
    """
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = -1
    return num
