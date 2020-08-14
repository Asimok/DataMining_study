# %%
import chardet
import requests

url = 'http://www.tipdm.com/tipdm/index.html'
rq = requests.get(url)
print('响应码', rq.status_code)
print("编码", rq.encoding)
print("请求头", rq.headers)

# rq.encoding 对context不生效
rq.encoding = 'utf-8'
print("实体1", rq.text)
# content 返回二进制字符串
print("实体2", rq.content.decode('utf-8'))

# 编码自动检测
su = chardet.detect(rq.content)
print(su)

# %%
# 完整请求过程
import chardet
import requests

# 网址
url = 'http://www.tipdm.com/tipdm/index.html'
# 请求头
head = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
                  'Safari/537.36'}

rq1 = requests.get(url, headers=head, timeout=2.0)
print("请求头", rq1.headers)
# 自动检测编码
# rq1.encoding = chardet.detect(rq.content).get('encoding')
rq1.encoding = chardet.detect(rq.content)['encoding']
print(rq1.text)

