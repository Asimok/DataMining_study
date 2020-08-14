import jieba
import pandas as pd


def data_process(file='/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/训练集.xlsx'):
    # file='/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/训练集.xlsx'
    classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
    data = pd.read_excel(file)
    data['一级分类'].value_counts()
    data_all = data['留言详情']
    data_labels = data['一级分类']
    labels_all = []
    for i in data_labels:
        labels_all.append(classification.index(i))

    # jieba 分词
    jieba.load_userdict('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/weibo_jieba.txt')
    data_cut = data_all.apply(lambda x: jieba.lcut(x))
    # 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
    stop_words = pd.read_csv('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/stopword.txt', encoding='GB18030',
                             sep='hhhhh')
    # pd转列表拼接  iloc[:,0] 取第0列
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n']
    data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])
    # 去除空格
    data_after_stop = data_after_stop.apply(lambda x: [i for i in x if i != ''])

    # 空格分割字符
    data_str = data_after_stop.apply(lambda x: ' '.join(x))

    return data_str, data_after_stop, labels_all
