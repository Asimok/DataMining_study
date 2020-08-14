import jieba
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
"""
训练集处理
"""
with open('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/stoplist.txt', 'r') as f:
    stop_words = f.read()  # 获取停顿词
f.close()
stop_words = ['  ', ' ', '\n','\t'] + stop_words.split()  # 改为列表 并且扩充一部分停顿词

replace_str=['，','。','.','!','：','（','）','、','‘','`','“','！','\\r\\n','\'',',','\\xa0','”','？','\'','；','?','\\']
classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
data_train = pd.read_excel('./data/训练集.xlsx', sheet_name='Sheet1')
text_tr = []
y_tr = []
jieba.load_userdict('./data/weibo.txt')
for i in data_train['留言详情']:
    string = str(i).strip().replace('\u3000', '')
    res = jieba.lcut(string, cut_all=False, HMM=True)
    tempstr = ''
    for j in res:
        for m in replace_str:
            # print(m)
            j=j.replace(m,'')
        if j not in stop_words:
            tempstr = tempstr + ' ' + j
    text_tr.append(tempstr)

for i in data_train['一级分类']:
    y_tr.append(classification.index(i))

# 文本转换成词频
vectorizer = CountVectorizer()
# 词频转换成权值矩阵
transformer = TfidfTransformer()

"""
测试集处理
"""
text_te = []
data_test = pd.read_excel('./data/测试集.xlsx', sheet_name='Sheet1')
for i in data_test['留言详情']:
    string = str(i).strip().replace('\u3000', '')
    res = jieba.lcut(string, cut_all=False, HMM=True)
    tempstr = ''
    for j in res:
        for m in replace_str:
            # print(m)
            j = j.replace(m, '')
        if j not in stop_words:
            tempstr = tempstr + ' ' + j
    text_te.append(tempstr)

"""
训练集样本
转成词向量
"""
count_tr = vectorizer.fit_transform(text_tr).toarray()
"""
权值矩阵
"""
tfidf_tr = transformer.fit_transform(count_tr).toarray()

"""
测试集样本
转成词向量
CountVectorizer(vocabulary=vectorizer.vocabulary_)保证测试集和训练集单词个数一致
"""
count_te = CountVectorizer(vocabulary=vectorizer.vocabulary_).fit_transform(text_te).toarray()
"""
权值矩阵
转成tf-idf权值
"""
tfidf_te = transformer.fit_transform(count_te).toarray()

# 高斯朴素贝叶斯模型
model =GaussianNB()
# 模型训练
model.fit(tfidf_tr, y_tr)
# 模型预测
ans = model.predict(tfidf_te)

print("真实数据      预测数据")
for i, j in zip(data_test['一级分类'], ans):
    print(i, "   ", classification[int(j)])



