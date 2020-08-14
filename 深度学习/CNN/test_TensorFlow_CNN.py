import cv2
import numpy as np
import tensorflow as tf

# 读取图片
img = cv2.imread('/home/asimov/PycharmProjects/DataMining/深度学习/CNN/1069099.png')
# img.shape
# 压缩图片 归一化
img = cv2.resize(img, (64, 64)) / 255
# img.shape

# 维度转换
# [1,64,64,3] 变成四维 一张图片 64*64 3层
img_new = np.float32(np.reshape(img, [1, 64, 64, 3]))

# filter 卷积核 3行 3列 3通道 32个
w1 = tf.random.normal([3, 3, 3, 32])

# 卷积操作
# strides=[1, 1, 1, 1] 移动步长1 padding='SAME' 用全0进行填充
conv1 = tf.nn.conv2d(input=img_new, filters=w1, strides=[1, 1, 1, 1], padding='SAME')
# print(conv1)

# 池化
# ksize=[1,2,2,1] filter 2*2  strides=[1,2,2,1] 移动步长2保障不取到重叠区域
pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
print(pool1)

# 绘画
sess = tf.Session()
conv = sess.run(conv1)
pool = sess.run(pool1)
sess.close()
# conv[0, :, :, 15]*500 第0个样本 所有行,所有列 第15面 放大500
cv2.imwrite('conv.jpg', conv[0, :, :, 15] * 500)  # 将卷积结果的某一个面可视化呈现
cv2.imwrite('pool.jpg', pool[0, :, :, 15] * 100)  # 将池化结果的某一个面可视化呈现
