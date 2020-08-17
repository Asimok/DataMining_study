import datetime



def get_date_interval(now, temp_start):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(temp_start, '%Y-%m-%d')

    d = (d1 - d2)
    # print('{}  比  {}  晚：{}天'.format(d1, d2, d.days))
    return d.days

a = get_date_interval('2020-03-21','2020-04-21')

import os
import pandas as pd
path='/Users/asimov/PycharmProjects/DataMining_study/大学生新闻中心/工作量统计/2020-03-01-2020-07-31  量化统计.xls'

info1 = pd.read_excel(path)
info1 = info1.drop_duplicates().reset_index(drop=True)
info1.to_excel(path)

name =['a','b']
name.remove('b')

a ='asdcvf'
a.index('sd')