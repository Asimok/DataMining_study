import pandas as pd
import requests
from lxml import etree

# 使用cookie保持登录
# cookies拼装成json


path = '/opt/mq/pytorch_study/dyjw\\'
Cookies = {"JSESSIONID": "8FD0CC9C157BD33AEA2743AA63693756"}
url_chengji = 'http://jwgl.nepu.edu.cn/xszqcjglAction.do?method=queryxscj'
url_getXueqi = 'http://jwgl.nepu.edu.cn/tkglAction.do?method=kbxxXs'
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36"}


# %%--------------------获取开课学期
rq_xueqi = requests.get(url=url_getXueqi, cookies=Cookies, headers=head)
html_xueqi = rq_xueqi.content.decode('utf8')
with open(path + 'rq_xueqi.html', 'w', encoding='utf8') as f:
    f.write(str(html_xueqi))
dom_xueqi = etree.HTML(html_xueqi, etree.HTMLParser(encoding='utf-8'))
# 学期列表
xueqi = dom_xueqi.xpath('//*[@id="xnxqh"]/option/text()')




# %%--------------------获取成绩
kkxq = {
    'kksj': xueqi[2],
    "kcxz": '',
    "kcmc": '',
    "xsfs": ''
}
rq_chengji = requests.get(url=url_chengji, cookies=Cookies, headers=head, params=kkxq)
html_chengji = rq_chengji.content.decode('utf8')
with open(path + 'rq_chnegji.html', 'w', encoding='utf8') as f:
    f.write(str(html_chengji))
dom_chengji = etree.HTML(html_chengji, etree.HTMLParser(encoding='utf-8'))
# 成绩查询结果
# 课程名
class_name = dom_chengji.xpath('//tr[@class="smartTr"][@class="smartTr"]/td[2]/text()')
# 成绩
score = dom_chengji.xpath('//tr[@class="smartTr"]/td[3]/a/text()')
# 课程性质
class_character = dom_chengji.xpath('//tr[@class="smartTr"]/td[4]/text()')
# 课程类别
class_category = dom_chengji.xpath('//tr[@class="smartTr"]/td[5]/text()')
# 学分
credit = dom_chengji.xpath('//tr[@class="smartTr"]/td[6]/text()')
columns = ["课程名称", "总成绩", "课程性质", "课程类别", "学分"]
my_score = pd.DataFrame(
    {"课程名称": class_name, "课程类别": class_category, "课程性质": class_character, "学分": credit,
     "总成绩": score}, columns=columns)
my_score.to_csv(path + '\成绩.csv', index=None)
