#逆向分析
import json
import pandas as  pd
import requests

url = 'https://www.ptpress.com.cn/bookinfo/getBookListForEBTag'
rq = requests.get(url)
# 获取json文件
data = json.loads(rq.content.decode("utf-8"))
# 列表推导式
author = [i['bookName'] for i in data['data']['data']]
price = [i['discountPrice'] for i in data['data']['data']]
# 格式化
ans = pd.DataFrame({'作者': author, '价格': price})
print(ans)
