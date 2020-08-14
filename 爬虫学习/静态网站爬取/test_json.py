# 数据存储
import json
import os

import requests
from bs4 import BeautifulSoup

url = 'http://www.tipdm.com/tipdm/index.html'
rq = requests.get(url)
soup = BeautifulSoup(rq.content, 'lxml')
data = soup.select('.menu>li>a')
names = [i.text for i in data]
href = [i['href'] for i in data]
# print(names)
# print(href)

# %% 写入json文件
import pandas as pd

with open('爬虫学习/静态网站爬取/temp.json', 'w') as f:
    json.dump({'name': names, 'href': href}, f, ensure_ascii=False)
# 查询当前工作路径
print(os.getcwd())
# 转换数据格式
a = pd.DataFrame({'name': names, 'href': href})
print(a)
