from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB

# 文本转换成词频
vectorizer = CountVectorizer()
# 词频转换成权值矩阵
transformer = TfidfTransformer()

# 训练集
text_tr = [
    'My dog has flea problems, help please.',
    'Maybe not take him to dog park is stupid.',
    'My dalmation is so cute. I love him my.',
    'Stop posting stupid worthless garbage.'
]
# 测试集
text_te = [
    'Mr licks ate mu steak, what can I do?.',
    'Quit buying worthless dog food stupid'
]

# 训练集样本标签
# 0积极 1消极
y_tr = [0, 1, 0, 1]
# 测试集样本标签
y_te = [0, 1]

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
print(ans)
