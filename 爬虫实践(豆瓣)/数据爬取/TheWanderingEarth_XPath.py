import re
import time

import pandas as pd
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 使用cookie保持登录
Cookie = 'll="118381"; bid=z4x8RO0iWK4; __utmz=30149280.1585827895.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ' \
         '_vwo_uuid_v2=D7F9E45C9BC497FFAF90644FC96F35587|78809323ec2ac880bcc8d1360986f266; ' \
         '__gads=ID=8bff95f98dcfa0d0:T=1585827965:S=ALNI_MYWYO4GK3KMFOqDgC2wGkgZBX_SBQ; ' \
         'dbcl2="155156279:hVzVl4WFc90"; ck=wX2-; ap_v=0,' \
         '6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1585837186%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport' \
         '%2Flogin%22%5D; _pk_ses.100001.8cb4=*; push_doumail_num=0; ' \
         '__utma=30149280.1860551383.1585827895.1585827895.1585837204.2; __utmc=30149280; __utmv=30149280.15515; ' \
         'push_noty_num=0; __utmt=1; __utmb=30149280.12.10.1585837204; __yadk_uid=pKalLG4tOjHMswZbXAKRQBoY7dQSBBhQ; ' \
         '_pk_id.100001.8cb4=8762e56344b9ba05.1585837186.1.1585838039.1585837186. '
Cookies = {}
for i in Cookie.split(';'):
    # 最多用一个=拆分
    key, value = i.split('=', 1)
    Cookies[key] = value
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36"}

driver = webdriver.Chrome()
url = 'https://movie.douban.com/subject/26266893/comments?start=20&limit=20&sort=new_score&status=P'
driver.get(url)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))


# 获取当前页面信息
def get_web_data(dom=None, Cookies=None, head=None):
    username = dom.xpath(
        '//div[@class="comment-item"]//span[@class="comment-info"]/a/text()')  # 用户名
    user_home = dom.xpath(
        '//div[@class="comment-item"]//span[@class="comment-info"]/a/@href')  # 用户主页
    star = dom.xpath(
        '//div[@class="comment-item"]//span[@class="comment-info"]/span[2]/@class')  # 评分
    comment_time = dom.xpath(
        '//div[@class="comment-item"]//span[@class="comment-info"]/span[@class="comment-time "]/@title')  # 评论时间
    comments = dom.xpath('//div[@class="comment-item"]//span[@class="short"]/text()')  # 评论内容
    greet_num = dom.xpath('//div[@class="comment"]//span[@class="votes"]/text()')  # 赞同数

    cities = []
    load_times = []
    for now_url in user_home:
        print('第', list(user_home).index(now_url), '个')
        user_data = requests.get(url=now_url, cookies=Cookies, headers=head)
        user_dom = etree.HTML(user_data.text, etree.HTMLParser(encoding='utf-8'))
        address = user_dom.xpath('//div[@class="user-info"]/a/text()')  # 用户居住地
        load_time = user_dom.xpath('//div[@class="user-info"]//div[@class="pl"]/text()')  # 加入时间
        cities.append(address)
        load_times.append(load_time)
        time.sleep(1)
    # 列表推导式
    star = ['' if 'rating' not in temp else int(re.findall('[0-9]{2}', temp)[0]) for temp in
            star]  # 匹配2个数字 comment-time 情况返回空
    load_times = ['' if temp == [] else temp[1].strip()[:-2] for temp in
                  load_times]  # 入会数据提取时间 '2007-01-11'
    cities = ['' if temp == [] else temp[0] for temp in cities]  # 把嵌套列表拿出来

    data = pd.DataFrame({'用户名': username, "居住城市": cities,
                         '加入时间': load_times, "评分": star, '发表时间': comment_time, '评论内容': comments,
                         '赞同数': greet_num})
    return data


all_data = pd.DataFrame()
wait = WebDriverWait(driver, 10)  # 等待10秒
i = 0
while i < 3:
    # 等待条件满足之后才进行下一步操作
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,
         '#comments > div:nth-child(1) > div.comment > h3 > span.comment-info > a')))
    html = driver.page_source
    dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
    res = get_web_data(dom, Cookies, head)
    all_data = pd.concat([all_data, res], axis=0)  # 数据拼接

    condition = driver.find_element_by_css_selector('#paginator > a.next')  # 寻找下一页按钮
    if not condition:
        break  # 已经到达最后一页
    confrim_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#paginator > a.next')))
    confrim_btn.click()  # 翻页
    i += 1
# 导出
all_data.to_excel('./data/douban.xlsx', encoding='GB18030')
