import pandas as pd
import pkuseg
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB

"""
训练集处理
"""
replace_str = ['，', '。', '.', '!', '：', '（', '）', '、', '‘', '`', '“', '！', '\\r\\n', '\'', ',', '\\xa0', '”', '？', '\'',
               '；', '?', '\\']
classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
data_train = pd.read_excel('训练集.xlsx', sheet_name='Sheet1')
text_tr = []
y_tr = []
pku = pkuseg.pkuseg(model_name='./models')

for i in data_train['留言详情']:
    string = str(i).strip().replace('\u3000', '')
    res = pku.cut(string)
    tempstr = ''
    for j in res:
        for m in replace_str:
            # print(m)
            j = j.replace(m, '')
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
data_test = pd.read_excel('测试集.xlsx', sheet_name='Sheet1')
for i in data_test['留言详情']:
    string = str(i).strip().replace('\u3000', '')
    res = pku.cut(string)
    tempstr = ''
    for j in res:
        for m in replace_str:
            # print(m)
            j = j.replace(m, '')
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
model = GaussianNB()
# 模型训练
model.fit(tfidf_tr, y_tr)
# 模型预测
ans = model.predict(tfidf_te)

print("真实数据      预测数据")
for i, j in zip(data_test['一级分类'], ans):
    print(i, "   ", classification[int(j)])
