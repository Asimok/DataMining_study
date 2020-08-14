

import re
# 要匹配的字符串对象
import time
#
# a="被赋予汗水和欢笑的日子将会成为她成长道路上最宝贵的回忆，祝福母校未来一定会更好！合照东北石油大学六十周年华诞倒计时49天飞扬的歌声，吟唱难忘的岁月，凝聚心头不变的情节；今天，我们用歌声共同挽起友爱的臂膀，让明天来倾听我们爱心旋律的唱响;期盼您下期观看《报答》。策划：吴波，郭连峰（校友），彭艳秋（校友）导演：吴波协调：曹建刚剪辑：吴波，王霖（助理团），李天赐（助理团）文字：郭雨仙，李泽月（助理团），张悦琳（助理团）" \
#   "大 学 生 新 闻 中 心 出 品\xa0图文编辑：刘\xa0\xa0\xa0岩责任编辑：王超颖审\u3000\u3000核：苍留松"
#
# # 匹配列表
# pattern=['(?<=图文编辑：).*?(?=责任编辑)','(?<=原创文字：).*?(?=责任编辑)','(?<=摄影记者：).*?(?=责任编辑)','(?<=视频制作：).*?(?=责任编辑)',
#          '(?<=图文编辑：).*?(?=原创文字)','(?<=原创文字：).*?(?=视频制作)','(?<=视频制作：).*?(?=图文编辑)',
#          '(?<=图文编辑：).*?(?=视频制作)','(?<=视频制作：).*?(?=摄影记者)','(?<=摄影记者：).*?(?=视频制作)',
#
#          ]
# # comment = re.compile('(?<=图文编辑：).*?(?=责任编辑)',re.S)
# name=[]
# for i in pattern:
#     comment = re.compile(i,re.S)
#     comment1 = comment.findall(a)
#     if len(comment1)>0:
#         name.append(comment1[0])
#
# name[0].replace('\xa0','')
# print(str(a).__contains__(comment))
#
# localtime = time.localtime(1595071935)
# dt = time.strftime('%Y-%m-%d %H:%M:%S', localtime)

import datetime




def get_date_interval(now, end):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(end, '%Y-%m-%d')

    d = (d1 - d2)
    print('{}  比  {}  晚：{}天'.format(d1, d2, d.days))
    return d.days

if get_date_interval('2020-07-20','2020-3-1')>=0:
    print('0k')
import pandas as pd
info1 =pd.read_excel('量化统计.xls')
info2=pd.read_excel('量化统计.xls')
info1 = pd.concat([info2,info2])
info1 =info1.drop_duplicates().reset_index(drop=True)
import os
os.path.exists('/opt/mq/pytorch_study/东油微博舆情监督/weibo.xls')

import jieba
jieba.load_userdict('姓名.txt')
def get_name(data):
    # 匹配列表
    pattern = ['图文编辑', '责任编辑', '原创文字', '责任编辑', '摄影记者', '视频制作', '原创图片', ':', '：', ' ', ' ']
    temp_name = []
    end_name = ''
    comment = re.compile('(?<=图文编辑：).*?(?=责任编辑)', re.S)
    comment1 = comment.findall(data)
    if len(comment1) > 0:
        p_name = str(comment1[0])
        p_name = ''.join(p_name.split())
        for i in pattern:
            p_name = p_name.replace(i, '')

        p_name = jieba.lcut(p_name)
        for j in p_name:
            end_name = end_name + " " + j
    return end_name


m = '图文编辑：向   波 责任编辑'
a = get_name(m)

# all = pd.read_excel('专业统计.xlsx')
# allname=all['姓名']
# allname.to_csv('姓名.txt',index=None,header=None)