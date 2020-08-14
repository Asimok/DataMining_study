import re

import requests

url = 'http://www.tipdm.com/tipdm/index.html'
rq = requests.get(url)
rq.encoding = 'utf-8'
# <li class=" on"><a href="/">首页</a></li>
# <li><a href="/tipdm/cpzx/" target="">产品中心</a></li>
# <li><a href="http://www.tipdm.com:80/xkjs/index.jhtml" target="">学科建设</a></li>
ans = re.findall('<li><a href="[a-z0-9.:/]+" target="">(.+)</a></li>', rq.text)
ans2=re.findall('<li[ a-z="]*><a href="[a-z0-9.:/]+".*>(.+)</a></li>', rq.text)
print(ans)
print(ans2)
