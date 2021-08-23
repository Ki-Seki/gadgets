"""
自动刷学习通课程的评论，
相关配置见 configuration.py
"""

from selenium import webdriver
import random
import time

import configuration

for url in configuration.reply_urls:
    driver = webdriver.Edge("MicrosoftWebDriver.exe")
    driver.get(url)

    # login
    elem_phone = driver.find_element_by_css_selector(".ipt-tel")
    elem_password = driver.find_element_by_css_selector(".ipt-pwd")
    elem_login = driver.find_element_by_css_selector("#loginBtn")
    elem_phone.send_keys(configuration.phone)
    elem_password.send_keys(configuration.password)
    elem_login.click()
    time.sleep(25)

    # auto comment
    elem_input = driver.find_element_by_css_selector(".replyEdit textarea")
    elem_submit = driver.find_element_by_css_selector(".addReply")
    for i in range(configuration.count):
        elem_input.clear()
        time.sleep(random.random() * 3)
        elem_input.send_keys(configuration.reply_content)
        time.sleep(random.random() * 3)
        elem_submit.click()
        time.sleep(random.random() * 3)

    driver.close()
