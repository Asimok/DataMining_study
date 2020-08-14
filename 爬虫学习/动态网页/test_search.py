# 使用python搜多图书信息
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.ptpress.com.cn/shopping/index'
driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)

# 定位窗口
before = driver.current_window_handle
print(driver.title)
# 通过selector查找搜索框

search_btn = driver.find_element_by_css_selector(
    'body > div.classifySearch-p > div > div.classifySearchBar > div.allSearch > input')
# 填写搜索内容
search_btn.send_keys("python编程")

# 显式等待条件  等待到元素可以被点击 通过selector 筛选路径
confrim_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                     'body > div.classifySearch-p > div > div.classifySearchBar > '
                                                     'div.allSearch > a > i')))
# 点击搜索按钮
confrim_btn.click()
# 移动到第二个窗口

driver.switch_to.window(driver.window_handles[1])
print(driver.title)
driver.get(driver.current_url)
time.sleep(4)
# 获取网页源代码
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

data = [i.text for i in soup.select('#search > div.book-floor > ul > li > p')]
print(data)
driver.close()
