import numpy as np
import torch

NUM_DIGITS = 10


def fizzbuzz_encode(i):
    if i % 15 == 0: return 3
    if i % 5 == 0: return 2
    if i % 3 == 0:
        return 1
    else:
        return 0


def fizzbuzz_decode(i, prediction):
    return [str(i), 'fizz', 'buzz', 'fizzbuzz'][prediction]


def helper(i):
    print(fizzbuzz_decode(i, fizzbuzz_encode(i)))


def binary_encode(i, num_digit):
    return np.array([i >> d & 1 for d in range(num_digit)][::-1])  # [::-1]翻转


trX = torch.Tensor([binary_encode(i, NUM_DIGITS) for i in range(101, 2 ** NUM_DIGITS)])
trY = torch.LongTensor([fizzbuzz_encode(i) for i in range(101, 2 ** NUM_DIGITS)])

NUM_HIDDEN = 100
model = torch.nn.Sequential(
    torch.nn.Linear(NUM_DIGITS, NUM_HIDDEN),
    torch.nn.ReLU(),
    torch.nn.Linear(NUM_HIDDEN, 4)
)

loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
# 模型训练代码
BATCH_SIZE = 120
for epoch in range(10000):
    for start in range(0, len(trX), BATCH_SIZE):
        end = start + BATCH_SIZE
        batchX = trX[start:end]
        batchY = trY[start:end]

        y_pred = model(batchX)  # forward
        loss = loss_fn(y_pred, batchY)

        optimizer.zero_grad()
        loss.backward()  # backpass
        optimizer.step()  # gradient descent
    print('Epoch', epoch, loss.item())


# 模型测试
testX = torch.Tensor([binary_encode(i,NUM_DIGITS) for i in range(1,101)])
with torch.no_grad():
    testY = model(testX)
predictions =zip(range(1,101),testY.max(1)[1].data.tolist())
PRE =[fizzbuzz_decode(i,x) for i,x in predictions]
# print(PRE)

ACT =[fizzbuzz_decode(i,fizzbuzz_encode(i))  for i in  range(1,101)]

t=0
for i in range(len(ACT)):
    if ACT[i]==PRE[i]:
        t+=1
acc = t/len(ACT)
print('准确率：',acc)