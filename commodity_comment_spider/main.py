import config

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Options to disable image loading
options = EdgeOptions()
options.use_chromium = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


# Jingdong Spider
def jd_spider(link):
    driver = Edge(options=options)
    driver.get(link)

    # Parsed data
    data = []

    # Get comment items of this page.
    comment_items = driver.find_elements(By.CSS_SELECTOR, '.tab-con .comment-item .comment-column.J-comment-column')
    for item in comment_items:
        # Get rate.
        star_elem = item.find_element(By.CSS_SELECTOR, '.comment-star')
        star = int(star_elem.get_attribute('class')[-1])
        # Get comment.
        comment_elem = item.find_element(By.CSS_SELECTOR, '.comment-con')
        comment = comment_elem.text.replace('<br/>', '\n')

        data.append((star, comment))
    driver.close()
    return data


# Taobao Spider
def taobao_spider(link):
    return []


# Save data to an Excel file.
def save_to_excel(data, filename):
    pass


def main():
    for link in config.commodity_links:
        data = []
        if 'jd.com' in link:
            data = jd_spider(link)
        elif 'taobao.com' in link:
            data = taobao_spider(link)
        save_to_excel(data, config.filename)


main()
