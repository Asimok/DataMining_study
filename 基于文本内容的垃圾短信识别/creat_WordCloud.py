from 基于文本内容的垃圾短信识别.data_process import data_process
from wordcloud import WordCloud
import matplotlib.pyplot as plt


data_str, data_after_stop, labels = data_process()
# 词频统计
word_fre = {}

for i in data_after_stop[labels == 0]:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1

# 绘制词云
mask = plt.imread('./data/duihuakuan.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc',mask=mask,background_color='white')
wc.fit_words(word_fre)
plt.imshow(wc)
plt.axis('off')
plt.show()
