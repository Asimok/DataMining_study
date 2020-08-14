import pandas as pd

data = pd.read_excel('./data/加票汇总.xlsx')
name = data['选手']
addTickes = data['票数']
data_new = pd.concat([name, addTickes], axis=1)


data_new2 = data_new.groupby(by='选手').sum()
data_new2.to_excel('data.xlsx')
data2=pd.read_excel('data.xlsx')
data_sort = data2.sort_values(by='票数',ascending=False)
data_sort.to_excel('data.xlsx')