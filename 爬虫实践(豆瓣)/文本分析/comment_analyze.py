# 数据预处理
from tkinter import _flatten
import jieba
import pandas as pd
import matplotlib.pyplot  as plt
from wordcloud import WordCloud

with open('../data/stoplist.txt', 'r') as f:
    stop_words = f.read()  # 获取停顿词
stop_words = ['', ' ', '\n'] + stop_words.split()  # 改为列表 并且扩充一部分停顿词
data = pd.read_csv('../data/douban.csv', encoding='GB18030')
data_cut = data['短评正文'].apply(jieba.cut)  # 分词
data_after = data_cut.apply(lambda x: [i for i in x if i not in stop_words])  # 去除停顿词
data_tuple = _flatten(list(data_after))  # 列表变为一维元组

word_fre = pd.Series(data_tuple).value_counts()  # 转为序列 统计词频
mask = plt.imread('../data/aixin.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', mask=mask, background_color='white')
wc.fit_words(word_fre)
plt.imsave('../data/img.png',wc)
plt.imshow(wc)
plt.axis('off')
plt.show()