import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel

pos_com = pd.read_csv('./data/pos_com.csv', header=None, index_col=0)
neg_com = pd.read_csv('./data/neg_com.csv', header=None, index_col=0)

# 正向评价
pos_com.columns = ['comment']
mid = list(pos_com['comment'].str.split(' '))
dictionary = Dictionary(mid)
bow = [dictionary.doc2bow(com) for com in mid]
# 模型构建
pos_model = LdaModel(corpus=bow, id2word=dictionary, num_topics=3)
pos_model.print_topic(0)
pos_model.print_topic(1)
pos_model.print_topic(2)

# 负面评价
neg_com.columns = ['comment']
mid = list(neg_com['comment'].str.split(' '))
dictionary = Dictionary(mid)
bow = [dictionary.doc2bow(com) for com in mid]
# 模型构建
neg_model = LdaModel(corpus=bow, id2word=dictionary, num_topics=3)
neg_model.print_topic(0)
neg_model.print_topic(1)
neg_model.print_topic(2)
