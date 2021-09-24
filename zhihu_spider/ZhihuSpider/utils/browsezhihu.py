import time
import pickle  # pickle 可以将 Python 对象的二进制数据存储为文件（即序列化）

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from ZhihuSpider import settings
from ZhihuSpider import privacy  # 包含不可以共享的配置内容

# 初始化一些参数，以便应对知乎的反爬机制
chrome_option = Options()
chrome_option.add_argument("--disable-extensions")
chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

browser = webdriver.Chrome(executable_path=settings.DRIVER_DIR, chrome_options=chrome_option)


def is_logged_in():
    return True
    # status = input("Are you logged in? (y/n)")
    # time.sleep(3)  # 防止 twisted 模块并行处理其他内容
    # if status in 'yY':
    #     return True
    # else:
    #     return False


def login():
    browser.find_element_by_css_selector(".SignFlow-tabs > div:nth-child(2)").click()  # 切换到密码输入
    browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
        Keys.CONTROL + "a")
    browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input"). \
        send_keys(privacy.ZHIHU_ACCOUNT)  # 输入账号
    browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
    browser.find_element_by_css_selector(".SignFlow-password input").send_keys(privacy.ZHIHU_PASSWORD)  # 输入密码
    browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()  # 点击登录
    time.sleep(5)  # 手动解决滑块验证码或其他验证码


def save_cookies():
    cookies = browser.get_cookies()
    pickle.dump(cookies, open(settings.ZHIHU_COOKIE_DIR, "wb"))


def get_cookies():
    """
    :return: 可以由 Scrapy 处理的 字典式 cookies
    """
    browser.get("https://www.zhihu.com/signin")
    if not is_logged_in():
        login()
    save_cookies()
    cookies = pickle.load(open(settings.ZHIHU_COOKIE_DIR, "rb"))  # 打开时是 rb，对应应该 wb
    cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    return cookie_dict
