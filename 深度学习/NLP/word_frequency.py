# 数据预处理
from tkinter import _flatten

import jieba
import matplotlib.pyplot  as plt
import pandas as pd
from wordcloud import WordCloud


def not_empty(s):
    return s and s.strip()


with open('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/stoplist.txt', 'r') as f:
    stop_words = f.read()  # 获取停顿词
f.close()
stop_words = ['  ', '', '\n', '\t'] + stop_words.split()  # 改为列表 并且扩充一部分停顿词
data = pd.read_excel('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/训练集.xlsx')
data_cut = data['留言详情'].apply(jieba.cut)  # 分词
data_after = data_cut.apply(lambda x: [i for i in x if i not in stop_words])  # 去除停顿词
data_after2 = []
for i in data_after:
    data_after2.append(list(filter(not_empty, list(i))))  # 去除空格
print(data_after2)
data_tuple = _flatten(data_after2)  # 列表变为一维元组
frequency = pd.Series(list(data_tuple)).value_counts()  # 转为序列 统计词频

mask = plt.imread('/home/asimov/PycharmProjects/DataMining/爬虫实践(豆瓣)/data/aixin.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', mask=mask, background_color='white')
wc.fit_words(frequency)
plt.imsave('img.png', wc)
plt.imshow(wc)
plt.axis('off')
plt.show()
