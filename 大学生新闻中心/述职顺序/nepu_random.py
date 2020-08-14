from random import shuffle
import pandas as pd
name = list(pd.read_excel('述职人员.xlsx')['姓名'])
shuffle(name)
for i in name:
    print(i)
for i, j in enumerate(name):
    name[i] = (i + 1).__str__() + ':' + j.__str__()
# print(name)
print("---述职随机顺序---")
for i in name:
    print(i)
