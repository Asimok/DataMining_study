import requests
from bs4 import BeautifulSoup

# lxml解析器
url = 'http://www.tipdm.com/tipdm/index.html'
rq = requests.get(url)
soup = BeautifulSoup(rq.content, 'lxml')
# print(soup.head)
# print(soup.body)

# %% 查找所有link
a = soup.link
# 返回字典类型
print(a['href'])
print(a.get('href'))

# %% findAll(标签)
print(soup.findAll('li'))

# %% find_all(class name)
a = soup.find_all('nav')
for i in a[0].find_all('li'):
    print(i.string)

# %% select(路径)
a = soup.select('html > head > title')[0]
print(a.text)

# %% select索引查找
a = soup.select('.menu>li')  # class
b = soup.select('#menu>li')  # id
# 列表推导式
ans = [i.text for i in a]
print(ans)

for i in soup.select('#menu > li.on > a'):
    print(i.text)

# %%搜狗搜索
url = 'https://weixin.sogou.com/'
rq2 = requests.get(url)
soup2 = BeautifulSoup(rq2.content, 'lxml')
ans = soup2.select('#topwords > li > a')
for i in ans:
    print(i.text)
b = soup2.find_all(id='topwords')[0]
print(b)
ans = [i.text for i in b.find_all('a')]
print(ans)
