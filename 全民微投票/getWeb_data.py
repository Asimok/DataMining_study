import re
import time

from http.cookiejar import LWPCookieJar
import pandas as pd
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# 保存Cookie
session = requests.Session()

# 使用cookie保持登录
Cookie = "UM_distinctid=1712e714cf0632-0ad91da0d053da-317a055e-1fa400-1712e714cf14f9; " \
         "Hm_lvt_d38909bba7c21cf2899b098ca6723fdc=1585834462,1585838775,1585880478,1586002806; " \
         "Qs_lvt_229460=1585834462%2C1585873817%2C1585915794%2C1585965068%2C1586002807; " \
         "mediav=%7B%22eid%22%3A%22107845%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22QD%60gmwxm9v9!%60NoLK'%22%2C%22ctn" \
         "%22%3A%22%22%2C%22vvid%22%3A%22QD%60gmwxm9v9!%60No%254cK'%22%7D; " \
         "CNZZDATA3782871=cnzz_eid%3D784740504-1585617207-https%253A%252F%252Fwww.qmwtp.com%252F%26ntime%3D1586014593" \
         "; CNZZDATA1260730015=1527997409-1585622109-https%253A%252F%252Fwww.baidu.com%252F%7C1586015776; " \
         "Qs_pv_229460=3263387356243967000%2C1704104608348216300%2C1003244234631251300%2C3129051009899741700" \
         "%2C2973068129325487000; ci_session=ui22gr4vj84ppe0t8309ohffn5rp5oik; " \
         "Hm_lpvt_d38909bba7c21cf2899b098ca6723fdc=1586015939 "
Cookies = {}
for i in Cookie.split(';'):
    # 最多用一个=拆分
    key, value = i.split('=', 1)
    Cookies[key] = value
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36"}
url= 'https://www.qmwtp.com/Center/votes_turnover?alias=pqpnjr96'
user_data = requests.get(url=url, cookies=Cookies, headers=head)
html=user_data.content.decode('utf8')
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
titles = dom.xpath('//tr[@class="smartTr"][@class="tr_one"]/td/text()')
username = dom.xpath('//tr[@class="smartTr"][@class="tr_two"]/text()')  # 用户名
