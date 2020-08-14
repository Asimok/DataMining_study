from pip._vendor.html5lib.treebuilders import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://jwgl.nepu.edu.cn/xszqcjglAction.do?method=queryxscj'
Cookies = {"JSESSIONID":"7EE6837479F9AD41B22BEA001ABD6C6C"}
driver = webdriver.Chrome()

driver.add_cookie(Cookies)
driver.get(url)

html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))

print(dom)
driver.close()
