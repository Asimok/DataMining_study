import matplotlib.pyplot as plt
import requests

# 保存Cookie
session = requests.Session()
url_login = 'http://jwgl.nepu.edu.cn/Logon.do?method=logon'
url_verifyCode = 'http://www.tipdm.org/captcha.svl'
head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36"}
path = 'E:\py_project\DataMining_study\dyjw'

# %%获取验证码

# 验证码保存路径
rq_verifyCode = requests.get(url_verifyCode)
with open(path + 'verifyCode.jpg', 'wb') as f:
    f.write(rq_verifyCode.content)
pic = plt.imread(path + 'verifyCode.jpg')
plt.imshow(pic)
plt.show()
verifyCode = input("请输入验证码\n")




# %%登录
login = {
    "USERNAME": '170703140113',
    "PASSWORD": '170703140113',
    "RANDOMCODE": verifyCode
}
rq_login = requests.post(url_login, data=login)
print(rq_login.status_code)
print(rq_login.url)
# 用session保持登录状态
newHtml = session.get(rq_login.url)
print(newHtml.content.decode('utf8'))
