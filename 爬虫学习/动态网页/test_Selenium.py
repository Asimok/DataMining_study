from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.ptpress.com.cn/shopping/index'
driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)
# 显式等待条件  等待到元素可以被点击 通过selector 筛选路径
confrim_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                     'body > div.classifySearch-p > div > div.classifySearchBar > '
                                                     'div.allSearch > a > i')))
print(confrim_btn)
driver.close()
