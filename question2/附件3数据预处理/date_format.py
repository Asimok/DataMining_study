"""
计算日期间隔
输入参数：
2个日期 date1, date2
返回参数：
日期间隔
"""
import datetime


def get_date_interval(date1, date2):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(date1, '%Y/%m/%d')
    d2 = datetime.datetime.strptime(date2, '%Y/%m/%d')

    d = -(d1 - d2)
    # print('{}  比  {}  早：{}天'.format(d1, d2, d.days))
    return d.days

# get_date_interval('2019/2/21 12:02:17', '2019/2/21 16:06:38')
