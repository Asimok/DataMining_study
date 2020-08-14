import os

import cv2
import numpy as np
import tensorflow as tf

path = 'testimages/'

tf.reset_default_graph()  # 重置计算图
sess = tf.Session()
# 导入保存好的计算图
saver = tf.train.import_meta_graph('model/softmax_model.meta')
# 导入计算图中的所有参数
saver.restore(sess, 'model/softmax_model')
graph = tf.get_default_graph()  # 获取当前计算图
input = graph.get_tensor_by_name('input:0')  # 模型输入节点
output = graph.get_tensor_by_name('output:0')  # 模型输出节点

pathDir = os.listdir(path)
pathDir.sort(key=lambda x:int(x.split('.')[0]))

for i in pathDir:
    # print(i)
    img = cv2.imread(path + str(i) )[:, :, 0] / 255  # 读取图片数据
    img = img.reshape([1, 28 * 28])  # 进行维度转化
    pre = sess.run(output, feed_dict={input: img})  # 将新样本放入模型中进行预测
    res = np.argmax(pre, 1)  # 预测标签
    print('图片 ', str(i) + ' 中的数字是: ', res[0])
sess.close()
