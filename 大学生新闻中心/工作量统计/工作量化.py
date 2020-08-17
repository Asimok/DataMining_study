import re

import pandas as pd
import jieba

name = pd.read_csv('姓名.txt', sep='\n',header=None)
data = pd.read_excel('2020-03-01-2020-07-31  量化统计.xls')

# 推送次数
push_name_txt = data['姓名']


def get_time(temp_class):
    push_name_list = []
    pattern = ['图文编辑：', '图片：', '文字：', '视频：', '原创文字：', '责任编辑：', '摄影记者：', '视频制作：', '图片制作：', '原创图片：', '投票制作：']
    pattern.remove(temp_class)
    temp_push_name_txt = []
    for i in push_name_txt:
        if str(i).__contains__(temp_class):
            temp_push_name_txt.append(str(i)[str(i).index(temp_class):])

    for i in temp_push_name_txt:
        is_contain = False
        for m in pattern:
            if str(i).__contains__(m):
                is_contain = True
        if is_contain:
            for j in pattern:
                comment = re.compile('(?<=' + temp_class + ').*?(?=' + j + ')', re.S)
                if len(comment.findall(i)) > 0:
                    push_name_list.append(comment.findall(i)[0])
                    break
        else:
            temp_push_name = str(i).replace(temp_class, '')
            if temp_push_name.__eq__('[]'):
                push_name_list.append('')
            else:
                push_name_list.append(temp_push_name)
    # 统计次数
    total_name = ''
    for i in push_name_list:
        total_name += str(i).strip()
    jieba.load_userdict('姓名.txt')
    total_name_list = jieba.lcut(total_name)
    temp_dict = dict(pd.Series(total_name_list).value_counts())
    return temp_dict


def get_score(temp_dict, weight):
    for i in temp_dict.keys():
        if i in score:
            score[i] += temp_dict[i] * weight
        else:
            score[i] = temp_dict[i] * weight
def get_score_push(temp_dict, weight):
    for i in temp_dict.keys():
        if i in score:
            score_push[i] += temp_dict[i] * weight
        else:
            score_push[i] = temp_dict[i] * weight

score = {}
score_push={}
# 推送次数/排版 1分
pushTime_name_dict = get_time('图文编辑：')
get_score_push(pushTime_name_dict, 1)
# 原创文字 3分
originalTime_name_dict1 = get_time('原创文字：')
get_score(originalTime_name_dict1, 3)
originalTime_name_dict2 = get_time('文字：')
get_score(originalTime_name_dict2, 3)
# 视频 4分
video_made_dict1 = get_time('视频制作：')
get_score(video_made_dict1, 4)
video_made_dict2 = get_time('视频：')
get_score(video_made_dict2, 4)
# 图片制作 2分
image_made_dict1 = get_time('图片制作：')
get_score(image_made_dict1, 2)
image_made_dict2 = get_time('图片：')
get_score(image_made_dict2, 2)
# 摄影记者 2分
photo_made_dict = get_time('摄影记者：')
get_score(photo_made_dict, 2)
# 投票制作 2分
vote_made_dict = get_time('投票制作：')
get_score(vote_made_dict, 2)

# 额外加分
# watches = data['浏览量']
# original = data['原创']
#
# for i in range(len(watches)):
#     if int(watches[i])>5000 and str(original[i]).__eq__('原创'):
#         print(watches[i])


# 分数计算

end_score = {}
end_score_push= {}
for i in list(name[0]):
    if i in score:
        end_score[i]= score.get(i)
    else:
        end_score[i] =0
for i in list(name[0]):
    end_score_push[i]= score_push.get(i)

pd.Series(end_score).to_excel('基础积分.xls')
pd.Series(end_score_push).to_excel('推送次数.xls')