import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 读取mnist数据集
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# 学习速率
learning_rate = 0.001
# 训练步长
train_step = 10000
# 每次训练放入的样本数量
batch_size = 100
# 打印间隔
displayer_step = 100
# 一个向量有多少元素
frame_size = 28
# 一共有多少向量
sequence_num = 28
# 隐藏神经元数量
hidden_size = 100
# 样本类别树 数字0-9 10个
n_class = 10

# 重置计算图
tf.reset_default_graph()

# 网络输入 x_data
# 占位符：模型输入
x_data = tf.placeholder(tf.float32, [None, frame_size * sequence_num], name='input')

"""
目标输出值
占位符：模型目标输出
"""
y_data = tf.placeholder(tf.float32, [None, n_class])

"""
输出层神经元权值
权值  tf.truncated_normal(shape=[hidden_size,n_class]) 符合正态分布
"""
weight = tf.Variable(tf.truncated_normal(shape=[hidden_size, n_class]))

"""
偏置项 设置为全0
输出层神经元阈值
"""
bias = tf.Variable(tf.zeros(shape=[n_class]))

"""
RNN 网络搭建
"""

# 改变样本外观形状
x = tf.reshape(x_data, shape=[-1, sequence_num, frame_size])
# 构建隐层循环结构 rnn_cell中设置100个神经元
rnn_cell = tf.nn.rnn_cell.BasicRNNCell(100)
# RNN传输过程
output, state = tf.nn.dynamic_rnn(rnn_cell, x, dtype=tf.float32)
"""
只需要最后一个输出
y 整个网络的输出值
"""
y = tf.nn.softmax(tf.matmul(output[:, -1, :], weight) + bias, name='output')

"""
交叉熵 cross_entropy
reduce_mean 均值
"""
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_data, logits=y))

"""
优化 AdamOptimizer 适量梯度优化器 
训练节点
"""
train = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
# 准确率
acc = tf.reduce_mean(tf.to_float(tf.equal(tf.argmax(y, 1), tf.arg_max(y_data, 1))))
# 保存模型
saver = tf.train.Saver()
#  启动会话
sess = tf.Session()
# 执行变量初始化操作
sess.run(tf.global_variables_initializer())

"""
训练 10000步
"""
step = 1
while step < train_step:
    # 获取训练样本
    x_s, y_s = mnist.train.next_batch(batch_size)
    # 模型训练
    loss, _ = sess.run([cross_entropy, train], feed_dict={x_data: x_s, y_data: y_s})
    if step % displayer_step == 0:
        # 模型训练精度
        acc_tr, loss = sess.run([acc, cross_entropy], feed_dict={x_data: x_s, y_data: y_s})
        print('第', step, '次训练', '训练精度', acc_tr, '交叉熵损失项', loss, )
    step += 1

# 测试模型在测试集上的预测精度
acc_te = sess.run(acc, feed_dict={x_data: mnist.test.images, y_data: mnist.test.labels})  # 模型测试精度
print('模型在测试集上的预测精度：', acc_te)
# 保存模型
saver.save(sess, 'model/softmax_model')
sess.close()
