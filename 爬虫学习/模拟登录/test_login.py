import matplotlib.pyplot as plt
import requests

# 保存Cookie
session = requests.Session()
# session = requests.Session()
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

rq = session.post(url=url, data=login)
# print(rq.status_code)
print(rq.url)
# 用session保持登录状态
# newHtml = session.get(rq2.url)
# print(newHtml.content.decode('utf8'))
