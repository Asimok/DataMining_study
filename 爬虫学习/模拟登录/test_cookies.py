import requests

# 使用cookie保持登录
# cookies拼装成json
Cookie = "uniqueVisitorId=93e5ebf5-b764-86f7-e506-08e706b90144; pgv_pvid=9254292048; _site_id_cookie=1; " \
         "JSESSIONID=B193C713D08823ABFA19B4AA146234D7; clientlanguage=zh_CN; __qc_wId=211; " \
         "JSESSIONID=B193C713D08823ABFA19B4AA146234D7; username=18182737073 "
Cookies = {}
for i in Cookie.split(';'):
    # 最多用一个=拆分
    key, value = i.split('=', 1)
    Cookies[key] = value
print(Cookies)
url = 'http://www.tipdm.org/member/index.jspx'
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36"}
rq = requests.get(url=url, cookies=Cookies, headers=head)
print(rq.content.decode('utf8'))
