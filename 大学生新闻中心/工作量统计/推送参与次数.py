import pandas as pd

all =pd.read_excel('量化统计.xls')
allname=list(all['姓名'])
allname_str=''
for i in allname:
    if i!="nan":
        allname_str=allname_str+''.join(str(i).split())
allname_str.replace('nan','')
import jieba
jieba.load_userdict('姓名.txt')
name =jieba.lcut(allname_str)
pd_name = pd.Series(name)
times = dict(pd_name.value_counts())
out =pd.Series(times)
out=out.sort_values(0,ascending=False)
out.to_excel('推送参与次数.xls')