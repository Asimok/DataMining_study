import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('../data/douban.csv', encoding='GB18030')

"""
《流浪地球》 豆瓣评分分布
"""
num = data['评分'].value_counts()
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.pie(num, autopct='%.2f %%', labels=num)  # 绘制饼图
plt.title('《流浪地球》 豆瓣评分分布')
plt.show()
print(matplotlib.matplotlib_fname())

"""
评论发表时间与时间的关系
"""
times = data['发表时间'].apply(lambda x: x.split(' ')[0]).value_counts()
sort_times=times.sort_index()  # 按日期排序
plt.plot(range(len(sort_times)), sort_times)
plt.xticks(range(len(sort_times)), sort_times.index, rotation=270)
plt.grid()
plt.title('评论发表时间与时间的关系')
plt.show()
