import time

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from 基于文本内容的垃圾短信识别.data_process import data_process

start = time.time()
data_str, data_after_stop, labels = data_process()

# 分割测试集 训练集
# 测试集占比20%
data_tr, data_te, labels_tr, labels_te = train_test_split(data_str, labels, test_size=0.20)

"""
---------------------------------模型------------------------------------
"""
# 文本转换成词频
countVectorizer = CountVectorizer()

# 获取训练集样本权值矩阵
data_tr = countVectorizer.fit_transform(data_tr)
x_tr = TfidfTransformer().fit_transform(data_tr.toarray()).toarray()
# 测试集样本权值矩阵
# 维度共享vocabulary=countVectorizer.vocabulary_
data_te = CountVectorizer(vocabulary=countVectorizer.vocabulary_).fit_transform(data_te)
x_te = TfidfTransformer().fit_transform(data_te.toarray()).toarray()

# 模型创建
model = GaussianNB()
# 模型训练
model.fit(x_tr, labels_tr)
# 模型预测
acr = model.score(x_te, labels_te)
# ans=model.predict(x_te)
print("精度：", acr)
# print(ans)

end = time.time()
print('运行时间：',end-start)
