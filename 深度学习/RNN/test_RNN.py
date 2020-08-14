import cv2
import numpy as np
import tensorflow as tf

img = cv2.imread('3.jpg')

# 取第0层 归一化
img = img[:, :, 0] / 255

# 转32位类型
img = np.float32(img)

# [-1,28,28] 1张图片 28*28
img = img.reshape([-1, 28, 28])
# 构建隐层循环结构 rnn_cell中设置100个神经元
rnn_cell = tf.nn.rnn_cell.BasicRNNCell(100)
# RNN传输过程
output, state = tf.nn.dynamic_rnn(rnn_cell, img, dtype=tf.float32)

#  启动会话
sess = tf.Session()
# 变量初始化
sess.run(tf.global_variables_initializer())
res = sess.run(output)
sess.close()
