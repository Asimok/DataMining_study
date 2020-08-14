import os
import pandas as pd
file = '/opt/mq/pytorch_study/嵌入式出勤\出勤'
fileList = os.listdir(file)
iot_1 = pd.read_excel("/opt/mq/pytorch_study/嵌入式出勤\物工171嵌入式系统出勤.xls")
iot1_name = list(iot_1.iloc[:,2][3:-2])
iot1_time =[]


def get_time(file):
    # temp = pd.read_excel(
    #     "E:\py_project\DataMining_study\嵌入式出勤\出勤\\2020-03-1108-00-52+0800CST-嵌入式系统-考勤记录.xlsx")
    temp = pd.read_excel(file)
    temp_name = list(temp.iloc[:, 3][3:])
    temp_time = list(temp.iloc[:, 7][3:])
    j = 0
    iot1_time_temp = []
    iot1_name_temp = []
    for index in range(len(temp_name)):
        for iot1_name_index in iot1_name:
            if str(temp_name[index]).__contains__(iot1_name_index):
                iot1_name_temp.append(temp_name[index])
                iot1_time_temp.append(str(temp_time[index]).replace("分钟", ''))
                j += 1
    print(j)
    iot1_time_2 = [0 for i in range(28)]
    for name in range(len(iot1_name)):
        for i in range(len(iot1_name_temp)):
            if str(iot1_name_temp[i]).__contains__(iot1_name[name]):
                iot1_time_2[name] = iot1_time_temp[i]
                break
            else:
                iot1_time_2[name] = 0
    iot1_time.append(iot1_time_2)

if __name__ == '__main__':
    for filenum in fileList:
        print(filenum)
        # temp=pd.read_excel(file+"/"+filenum)
        # temp_name=temp.iloc[:,3][3:-2]
        get_time(file+"/"+filenum)

df = pd.DataFrame(i for i in iot1_time)
all_time=pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
name = pd.DataFrame(iot1_name)
all_time.insert(0, 'E', name)
all_time.to_excel('/opt/mq/pytorch_study/嵌入式出勤\时间.xls',index=None,header=None)