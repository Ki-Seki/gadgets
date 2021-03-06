"""
自动刷学习通课程的评论，仅支持旧版的学习通
学习通的讨论页
相关配置见 configuration.py
"""

import random
import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import configuration as conf


# 驱动实例化
driver = webdriver.Edge("msedgedriver.exe")
driver.maximize_window()  #浏览器最大化

# 登录
driver.get(conf.login_url)
elem_phone = driver.find_element_by_css_selector(".ipt-tel")
elem_password = driver.find_element_by_css_selector(".ipt-pwd")
elem_login = driver.find_element_by_css_selector("#phoneLoginBtn")
elem_phone.send_keys(conf.phone)
elem_password.send_keys(conf.password)
elem_login.click()

# 检查是否登录上
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, 'space_nickname')))

for url in conf.discuss_urls:
    driver.get(url)
    for index in range(conf.count):
        # 添加话题
        time.sleep(random.random() * 3)
        add_topic = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'c_title')))
        add_topic.send_keys(conf.reply_content[random.randint(0, len(conf.reply_content)-1)])

        # 提交
        time.sleep(random.random() * 3)
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.qdBtn')))
        time.sleep(random.random() * 3)
        try:
            submit.click()
        except ElementNotInteractableException:
            submit.click()  # 有时候因为没有加载完毕可能需要再点击一次
        
        # 跳过对话框
        time.sleep(random.random() * 3)
        alert = driver.switch_to.alert
        alert.dismiss()

        print(f'已发送 {index + 1} 条')

driver.close()
