from http.cookiejar import LWPCookieJar
import matplotlib.pyplot as plt
import requests

# 保存Cookie
session = requests.Session()
# 创建cookie实例
session.cookies = LWPCookieJar('cookie')

# 验证码
captcha = 'http://www.tipdm.org/captcha.svl'
# 验证码保存路径
path = 'captcha/'
rq = session.get(captcha)
with open(path + 'captcha.jpg', 'wb') as f:
    f.write(rq.content)
pic = plt.imread(path + 'captcha.jpg')
plt.imshow(pic)
plt.show()
captcha_code = input("请输入验证码\n")

# 模拟登陆
url = 'http://www.tipdm.org/login.jspx'
login = {'username': '18182737073', 'password': '1239877mq', 'captcha': captcha_code}
rq2 = session.post(url, data=login)
# 登录状态
print(rq2.status_code)
# 跳转网页
print(rq2.url)
# 保存cookie
session.cookies.save(ignore_discard=True, ignore_expires=True)

# 加载保存的cookie
session.cookies.load(ignore_discard=True, ignore_expires=True)
# 用session保持登录状态
newHtml = session.get('http://www.tipdm.org/member/index.jspx')
with open('newHtml.html', 'w',encoding='utf8') as f:
    f.write(newHtml.content.decode('utf8'))
f.close()
