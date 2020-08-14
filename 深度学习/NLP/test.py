import pandas as pd

data = pd.read_csv('/home/asimov/PycharmProjects/DataMining/基于文本内容的垃圾短信识别/data/message80W1.csv', header=None, index_col=0)
data.columns = ['label', 'message']
data['label'].value_counts()
