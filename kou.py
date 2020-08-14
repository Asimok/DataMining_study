import  pandas as pd

data = pd.read_excel('抠.xlsx')
sex = data['sex']
sex.value_counts()
age = data['age']
age_vc = age.value_counts(sort=False)
age_vc_list = dict(age_vc)
man = data[data['sex']== '男']
age_vc_man = man['age'].value_counts(sort=False)
woman = data[data['sex']== '女']
age_vc_woman = woman['age'].value_counts(sort=False)
age_vc_man_list = dict(age_vc_man)
age_vc_woman_list = dict(age_vc_woman)
# 男
proportion_man={}
for key in age_vc_man_list.keys():
    proportion_man[key]=age_vc_man_list.get(key)/age_vc_list.get(key)

print('male',proportion_man)
# 女
proportion_woman={}
for key in age_vc_woman_list.keys():
    proportion_woman[key]=age_vc_woman_list.get(key)/age_vc_list.get(key)
print('female',proportion_woman)