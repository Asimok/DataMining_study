import urllib3

# %%

http = urllib3.PoolManager()
rq = http.request('GET', url='http://www.tipdm.com/tipdm/index.html')
print("服务器响应码", rq.status)
# print("响应实体", rq.data)

# %%

http = urllib3.PoolManager()
head = {'User-Agent': 'Windows NT 6.1; Win64; x86'}
rq = http.request('GET', url='http://www.tipdm.com/tipdm/index.html', headers=head)
print("服务器响应码", rq.status)

# %%

# timeout 浮点数　响应超时时间　3.0秒
http = urllib3.PoolManager()
head = {'User-Agent': 'Windows NT 6.1; Win64; x86'}
rq = http.request('GET', url='http://www.tipdm.com/tipdm/index.html', headers=head, timeout=3.0)

# urllib3.Timeout() 连接和读取超时时间
http = urllib3.PoolManager()
head = {'User-Agent': 'Windows NT 6.1; Win64; x86'}
rq = http.request('GET', url='http://www.tipdm.com/tipdm/index.html', headers=head,
                  timeout=urllib3.Timeout(connect=1.0, read=3.0))

# 连接超时时间
http = urllib3.PoolManager(timeout=3.0)
rq = http.request('GET', url='http://www.tipdm.com/tipdm/index.html')
print("服务器响应码", rq.status)

# %%

# retries 重试次数,redirect 重定向
# retrirs=false 同时关闭请求重试和重定向
http = urllib3.PoolManager(timeout=3.0, retrirs=False)
# retrirs=10 重试10次
http = urllib3.PoolManager(timeout=3.0, retrirs=10)

# %%
# 完整请求过程

# 发送请求实例
http = urllib3.PoolManager()
# 网址
url = 'http://www.tipdm.com/tipdm/index.html'
# 请求头
head = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
                  'Safari/537.36'}
# 超时时间
tm = urllib3.Timeout(connect=1.0, read=3.0)
# 重试次数和重定向次数
rq = http.request('GET', url=url, headers=head, timeout=tm, retries=5, redirect=4)
print("服务器响应码", rq.status)
print("响应实体", rq.data.decode('utf-8'))
