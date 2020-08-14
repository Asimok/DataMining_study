import jieba

# 测试jieba分词

str = "南门街前段时间经过整改劝阻摆摊占道的情况改善了很多，但是情况好了几天又慢慢的和以前一样了，只要有人带头 " \
      "后面慢慢又摆出来，很多商户现在干脆用钩子把一些货物挂门口屋檐下的电线上，上有政策下就有对策，城管来检查就稍微" \
      "好点，城管一走又摆出来又是老样子，希望有关部门采取强硬点的措施，每次都不痛不痒的整治一下根本起不到什么效果。现在二小门口那条路也成了马路市场了，卖小菜.卖鱼的.卖水果的成堆了。 "
# 添加词组
# jieba.add_word('南门街')
# 批量添加
jieba.load_userdict('./data/weibo_jieba.txt')

# 不使用全切割 使用隐马模型
res = jieba.lcut(str, cut_all=False, HMM=True)
print(str)
print(res)

a = ''
for i in res:
    a = a + ' ' + i.replace('，', '').replace('。', '').replace('.', '')
print(a)
data=[]
with open('/home/asimov/PycharmProjects/DataMining/深度学习/NLP/data/weibo_jieba.txt','r') as f:
   data.append(f.read())
f.close()
with open('weibo.txt','w') as f:
    for i in data[0].split(' '):
        i.strip()
        if i.split():
            f.write(i+'\n')
            print(i)