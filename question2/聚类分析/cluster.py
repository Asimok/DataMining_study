"""
对预处理后的附件三留言详情进行聚类分析
输入参数：
DBSCAN 参数 ，热度指数求解参数
输入文件：
去除30天内同一用户相似度0.75+的留言.xls
输出文件：
聚类结果明细表.xls
表2-热点问题留言明细表.xls
"""
import re

import jieba.analyse
import jieba.analyse
import jieba.posseg as psg
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from textrank4zh import TextRank4Sentence



print('开始进行聚类分析')
# DBSCAN 参数
temp_eps = 0.9
temp_min_sampleses = 4
# 热度指数求解参数


path = '/opt/mq/pytorch_study/东油微博舆情监督/weibo.xls'
message_data = pd.read_excel(path)
all_data = pd.read_excel(path)
predict_data1 = message_data['微博内容'][0:982].astype(str)
predict_data = []
comment = re.compile(r'#.*#', re.S)
for i in predict_data1:

    comment1 = comment.findall(i)
    if len(comment1) > 0:
        s = i.replace(comment1[0], '')
        predict_data.append(s)
    else:
        predict_data.append(i)

data_cut = pd.Series(predict_data).astype(str).apply(lambda x: jieba.lcut(x))
# 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
stop_words = pd.read_csv('/opt/mq/pytorch_study/question2/data/stopword.txt', sep='hhhh',
                         encoding='GB18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0].astype(str)) + [' ', '...', '', '  ', '→', '-', '：', ' ●',
                                                        '\t', '\n', '！', '？','nan']

word2flagdict = {}
data_after_jieba = []
for temp_theme in predict_data:
    data_cut = psg.cut(temp_theme)
    data_after_stop = []
    for i in data_cut:
        if i.word not in stop_words:
            if i.word != "":
                data_after_stop.append(i.word)
                word2flagdict[i.word] = i.flag
    keywords = " ".join(data_after_stop)
    data_after_jieba.append(keywords)
# all_data['主题分词'] = data_after_jieba
# all_data.to_excel('../聚类分析/附件3_labels.xlsx', index=None)
# 造一个{“词语”:“词性”}的字典，方便后续使用词性
# 短文本特征提取
vectorizer = CountVectorizer()
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(data_after_jieba))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 我们将word中每个词语的词性，通过自定义的方式赋给它们不同的权重，并乘到weight上的每一行样本中，
# 进而改变它们的特征矩阵。这样做的目的其实是想让特征矩阵的区分能力增强一点，代码如下所示：
wordflagweight = [1 for i in range(len(word))]  # 这个是词性系数，需要调整系数来看效果
for i in range(len(word)):
    if word2flagdict.get(word[i]) == "n":  # 这里只是举个例子，名词重要一点，我们就给它1.1
        wordflagweight[i] = 1.0
    # elif word2flagdict.get(word[i]) == "ns":
    #     wordflagweight[i] = 1.1
    else:  # 权重数值还要根据实际情况确定，更多类型还请自己添加
        continue

wordflagweight = np.array(wordflagweight)
new_weight = weight.copy()
for i in range(len(weight)):
    for j in range(len(word)):
        new_weight[i][j] = weight[i][j] * wordflagweight[j]

# DBSCAN聚类分析

DBS_clf = DBSCAN(eps=temp_eps, min_samples=temp_min_sampleses)
DBS_clf.fit(new_weight)
labels_ = DBS_clf.labels_


# === Define the function of classify the original corpus according to the labels === #
def labels_to_original(labels, original_corpus):
    assert len(labels) == len(original_corpus)
    max_label = max(labels)
    number_label = [i for i in range(0, max_label + 1, 1)]
    number_label.append(-1)
    result = [[] for i in range(len(number_label))]
    result_loc = [[] for i in range(len(number_label))]
    for labels_loc in range(len(labels)):
        res_index = number_label.index(labels[labels_loc])
        result[res_index].append(original_corpus[labels_loc])
        result_loc[res_index].append(labels_loc)
    return result, result_loc


labels_original, labels_loc = labels_to_original(labels_, data_after_jieba)

theme_data=[]
for i in labels_loc:
    temp_theme=[]
    for j in i:
        tp =predict_data[j]
        if len(tp)>0:
            temp_theme.append(tp)
    theme_data.append(temp_theme)

question_list=theme_data
themw_abb=[]

for question_id in question_list:

    title = '\n'.join(question_id)
    sentence = TextRank4Sentence(delimiters='\n')
    sentence.analyze(text=title, lower=True)
    abstract = '\n'.join([item.sentence for item in sentence.get_key_sentences(num=1)])
    themw_abb.append(abstract)
    print("主题句为：", abstract)

pd.Series(themw_abb).to_excel('热点话题.xls',header=None)

# 活跃用户
user = message_data['用户名称'][0:982].astype(str)
pd.Series(user.value_counts()).to_excel('活跃用户.xls',header=None)
# 最火微博
all_data = pd.read_excel(path)[0:982]
all_data =all_data.sort_values(by="微博评论量" , ascending=False)
pd.DataFrame({'用户名称':all_data['用户名称'],'微博内容':all_data['微博内容'],'微博转发量':all_data['微博转发量'],
              '微博评论量': all_data['微博评论量'],'微博点赞':all_data['微博点赞']}).to_excel('最火微博.xls',header=None)