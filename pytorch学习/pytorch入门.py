import numpy as np
import matplotlib.pyplot as plt
N, D_in, H, D_out = 64, 1000, 100, 10

# 神经网络
# h=w1x
# a=max(0,h)  relu函数
# y=w2a

# 随机创建一些训练数据
x = np.random.randn(N, D_in)
y = np.random.randn(N, D_out)

w1 = np.random.randn(D_in, H)
w2 = np.random.randn(H, D_out)

learning_rate = 1e-6
loss_acc =[]
for it in range(500):
    # forward pass
    h = x.dot(w1)  # N*H
    h_relu = np.maximum(h, 0)  # N*H
    y_pred = h_relu.dot(w2)  # N*D_out

    # compute loss
    loss = np.square(y_pred - y).sum()
    loss_acc.append(loss)
    print(it, loss)

    # Backward pass
    # compute the gradient
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.T.dot(grad_y_pred)
    grad_h_relu = grad_y_pred.dot(w2.T)
    grad_h = grad_h_relu.copy()
    grad_h[h<0] = 0
    grad_w1 = x.T.dot(grad_h)

    # update weights of w1 and w2
    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2

# 生成图形
plt.plot(loss_acc)
plt.savefig('b.jpg')
