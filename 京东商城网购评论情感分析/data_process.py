import re

import jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

data = pd.read_csv('./data/comment.csv')
y = data['品牌'].value_counts()
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.bar(range(len(y)), y)
plt.xticks(range(len(y)), y.index)
# plt.show()

# 评论预处理
data_AO = data[data['品牌'] == 'AO']['评论']
cls = data[data['品牌'] == 'AO']['型号'].value_counts().index
# 踢出换行符 dropna()去除空值
data_AO = data_AO.dropna().apply(lambda x: re.sub('\n', '', x))
# 剔除型号
data_AO = data_AO.apply(lambda x: re.sub('AO史密斯（A.O.Smith） ET[0-9]+J-[0-9]+ 电热水器 [0-9]+升', '', x))
# 踢除HTML中表情符号  &+字母+；（&hellip;）
data_AO = data_AO.apply(lambda x: re.sub('&[a-zA-Z]+;', '', x))
# 剔除颜文字( ^_^ )
data_AO = data_AO.apply(lambda x: re.sub('\\(.*\\)', '', x))

# 文本去重
data_AO.drop_duplicates(inplace=True)
# 分词
data_cut = data_AO.apply(jieba.lcut)
# 去除停用词
stopWord = pd.read_csv('./data/stopword.txt', sep='hhhh', encoding='GB18030')
stopWords = list(stopWord.iloc[:, 0]) + [' ']
data_after_stopWords = data_cut.apply(lambda x: [i for i in x if i not in stopWords])
# 去除空行
index = data_after_stopWords.apply(lambda x: len(x) != 0)
data_after_stopWords_mot_null = data_after_stopWords[index]
# 统计词频
dic = {}
for i in data_after_stopWords_mot_null:
    for j in i:
        if j not in dic.keys():
            dic[j] = 1
        else:
            dic[j] += 1
# dic.pop(' ')

mask = plt.imread('./data/duihuakuan.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', mask=mask, background_color='white')
wc.fit_words(dic)
plt.imshow(wc)
plt.axis('off')
plt.show()
"""
----------------------------------- 情感分析-----------------------------------
"""
score = pd.read_csv('./data/BosonNLP_sentiment_score.txt', sep=' ', header=None)
score.columns = ['word', 'score']
degree = pd.read_csv('./data/degree.csv')
not_word = pd.read_csv('./data/not.csv')
degree['score'] = -degree['score'] / 100
not_word['score'] = -1  # 初始分数


def getScore(x=None):
    t = pd.DataFrame(x)
    t.columns = ['word2']
    t_score = pd.merge(t, score, how='left', left_on='word2', right_on='word')
    # 考虑程度副词的影响 程度副词修饰后一个词
    tmp = pd.merge(t_score, degree, how='left', left_on='word2', right_on='term')
    in_degree = tmp['term'].notnull()
    in_degree2 = in_degree.index[in_degree]
    for i in in_degree2:
        if i != len(tmp) - 1:
            tmp.loc[i + 1, 'score_x'] = tmp.loc[i, 'score_y'] * tmp.loc[i + 1, 'score_x']

    # 考虑否定词的影响 程度副词修饰后一个词 乘-1
    tmp1 = pd.merge(tmp, not_word, how='left', left_on='word2', right_on='term')
    in_degree = tmp1['term_y'].notnull()
    in_degree2 = in_degree.index[in_degree]
    for i in in_degree2:
        if i != len(tmp1) - 1:
            tmp1.loc[i + 1, 'score_x'] = tmp1.loc[i, 'score_y'] * tmp1.loc[i + 1, 'score_x']
    temp_score = tmp1['score_x'].sum()
    return temp_score


score = data_after_stopWords_mot_null.apply(getScore)
# 空格分隔
message = data_after_stopWords_mot_null.apply(lambda x: ' '.join(x))

index_loc = score > 0
message[index_loc].to_csv('./data/pos_com.csv')
message[-index_loc].to_csv('./data/neg_com.csv')
