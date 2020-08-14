import  torch.nn as nn
import torch
N, D_in, H, D_out = 64, 1000, 100, 10
# 随机创建一些训练数据
x = torch.randn(N, D_in)
y = torch.randn(N, D_out)

model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H, bias=False), # w_1 * x + b_1
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out, bias=False),
)

torch.nn.init.normal_(model[0].weight)
torch.nn.init.normal_(model[2].weight)

# model = model.cuda()

loss_fn = nn.MSELoss(reduction='sum')

learning_rate = 1e-6
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

for it in range(500):
    # Forward pass
    y_pred = model(x) # model.forward()

    # compute loss
    loss = loss_fn(y_pred, y) # computation graph
    print(it, loss.item())

    optimizer.zero_grad()
    # Backward pass
    loss.backward()

    # update model parameters
    optimizer.step()

import scipy