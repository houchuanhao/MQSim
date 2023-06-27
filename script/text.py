import torch
import torch.nn as nn
import torch.optim as optim

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.hidden_layer = nn.Linear(input_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.hidden_layer(x))
        x = self.output_layer(x)
        return x

input_size = 10
hidden_size = 20
output_size = 1

# 创建神经网络实例
net = NeuralNetwork(input_size, hidden_size, output_size)

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.01)

batch_size = 5
input_data = torch.randn(1, input_size)
target_data = torch.randn(batch_size, output_size)

output = net(input_data)
print(input_data)
print(output)


if False:
    # 前向传播
    output = net(input_data)

    # 计算损失
    loss = criterion(output, target_data)

    # 反向传播和参数更新
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()