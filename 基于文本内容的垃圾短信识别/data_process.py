import re

import jieba
import pandas as pd


def data_process(file='./data/message80W1.csv'):
    """
    垃圾短信 0 720000
    正常短信 1 80000
    """
    # header=None 没有列名 header=None 第0行是行索引
    data = pd.read_csv(file, header=None, index_col=0)
    data.columns = ['label', 'message']
    data['label'].value_counts()
    """
    ------------------------------1.数据抽样--------------------------------------
    """
    n = 20000
    a = data[data['label'] == 0].sample(n)  # 垃圾短信
    b = data[data['label'] == 1].sample(n)  # 正常短信

    """
    数据拼接
    两个Series的拼接，默认是在列上(往下)拼接，axis = 0,如果要横向往右拼接，axis = 1
    """
    data_new = pd.concat([a, b], axis=0)

    """
    ------------------------------2.数据预处理-------------------------------------
    """
    # 数据去重复
    data_dup = data_new['message'].drop_duplicates()
    # 数据脱敏(去除x序列)
    data_qumin = data_dup.apply(lambda x: re.sub('x', '', x))
    # jieba 分词
    jieba.load_userdict('./data/newdic1.txt')
    data_cut = data_qumin.apply(lambda x: jieba.lcut(x))
    # 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
    stop_words = pd.read_csv('./data/stopword.txt', encoding='GB18030', sep='hhhhh', header=None)
    # pd转列表拼接  iloc[:,0] 取第0列
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '→', '-', '：', ' ●']
    data_after_stop = data_cut.apply(lambda x: [i for i in x if i not in stop_words])
    # 对应短信的状态
    labels = data_new.loc[data_after_stop.index, 'label']
    # 空格分割字符
    data_str = data_after_stop.apply(lambda x: ' '.join(x))

    return data_str, data_after_stop, labels


