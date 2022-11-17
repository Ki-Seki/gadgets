"""
自动刷学习通课程的评论，仅支持旧版的学习通
学习通的讨论页
相关配置见 configuration.py
"""

import random
import time
import datetime

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import configuration as config


def is_element_present(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
    except NoSuchElementException:
        return False
    return True


def reserve(conf):
    succeed = False
    trial = 0
    while not succeed and trial < conf.max_trial:
        # 驱动实例化
        driver = webdriver.Edge("msedgedriver.exe")
        driver.maximize_window()  # 浏览器最大化

        # 登录
        driver.get(conf.url)
        # time.sleep(random.random() * 2)
        # time.sleep(1)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[onclick]')))
        driver.find_element(By.CSS_SELECTOR, 'li[onclick]').click()
        # time.sleep(random.random() * 1
        time.sleep(1)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.lg_form input[name=id]')))
        driver.find_element(By.CSS_SELECTOR, '.lg_form input[name=id]').send_keys(conf.id)
        driver.find_element(By.CSS_SELECTOR, '.lg_form input[name=pwd]').send_keys(conf.pwd)
        driver.find_element(By.CSS_SELECTOR, '.lg_form input[value=登录]').click()
        # time.sleep(random.random() * 2)
        # time.sleep(1)

        # 跳转到预定研讨间页面
        time.sleep(3)
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.it_list li')))
        driver.find_elements(By.CSS_SELECTOR, 'ul.it_list li')[8].click()
        # time.sleep(random.random() * 2)
        # time.sleep(1)

        date_str = (datetime.date.today() + datetime.timedelta(days=conf.date_delta)).strftime('%Y-%m-%d')
        date_selector = f'td[date="{date_str}"]'
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_selector)))
        driver.find_element(By.CSS_SELECTOR, date_selector).click()
        # time.sleep(random.random() * 2)
        # time.sleep(1)

        # 拖曳选择时间
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[objname="{conf.room}"] tr td[hour="7"]')))
        src = driver.find_element(By.CSS_SELECTOR, f'div[objname="{conf.room}"] tr td[hour="7"]')
        tgt = driver.find_element(By.CSS_SELECTOR, f'div[objname="{conf.room}"] tr td[hour="8"]')
        AC(driver).drag_and_drop(src, src).perform()
        # AC(driver).drag_and_drop_by_offset(src, 100, 0)

        # 预定详情页
        ## 消除某些情况下的弹窗
        # driver.find_element(By.CSS_SELECTOR, '#ui-id-2').click()
        # time.sleep(random.random() * 2)
        # time.sleep(1)
        ## 搜索成员并选定
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id^="dlg_resv_panel_default"] input.mb_name_ipt')))
        driver.find_element(By.CSS_SELECTOR, 'div[id^="dlg_resv_panel_default"] input.mb_name_ipt').send_keys(
            conf.partner)
        # time.sleep(random.random() * 3)
        # time.sleep(2)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul#ui-id-1 li')))
        driver.find_element(By.CSS_SELECTOR, 'ul#ui-id-1 li').click()
        ## 选择开始时间
        st_select = driver.find_elements(By.CSS_SELECTOR, '[name="start_time"]')[-1]
        Select(st_select).select_by_visible_text(conf.st)
        ## 选择结束时间
        ed_select = driver.find_elements(By.CSS_SELECTOR, '[name="end_time"]')[-1]
        Select(ed_select).select_by_visible_text(conf.ed)
        ## 填写申请理由
        driver.find_element(By.TAG_NAME, 'textarea').send_keys(conf.desc)
        ## 提交
        driver.find_element(By.CSS_SELECTOR, 'input[value="提交"]').click()
        # time.sleep(2)

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'ui-id-4')))
        succeed = is_element_present(driver, By.ID, 'ui-id-4')
        driver.close()
        trial += 1
    return succeed


if __name__ == '__main__':
    time_start=time.time()

    if reserve(config):
        print('Succeed!')
    else:
        print('Fail!')

    time_end = time.time()
    print('time cost', time_end - time_start, 's')

# elem_phone = driver.find_element_by_css_selector(".ipt-tel")
# elem_password = driver.find_element_by_css_selector(".ipt-pwd")
# elem_login = driver.find_element_by_css_selector("#phoneLoginBtn")
# elem_phone.send_keys(conf.phone)
# elem_password.send_keys(conf.password)
# elem_login.click()
#
# # 检查是否登录上
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.ID, 'space_nickname')))
#
# for url in conf.discuss_urls:
#     driver.get(url)
#     for index in range(conf.count):
#         # 添加话题
#         time.sleep(random.random() * 3)
#         add_topic = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'c_title')))
#         add_topic.send_keys(conf.reply_content[random.randint(0, len(conf.reply_content) - 1)])
#
#         # 提交
#         time.sleep(random.random() * 3)
#         submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.qdBtn')))
#         time.sleep(random.random() * 3)
#         try:
#             submit.click()
#         except ElementNotInteractableException:
#             submit.click()  # 有时候因为没有加载完毕可能需要再点击一次
#
#         # 跳过对话框
#         time.sleep(random.random() * 3)
#         alert = driver.switch_to.alert
#         alert.dismiss()
#
#         print(f'已发送 {index + 1} 条')
#
# driver.close()
