import torch.nn as nn
#from collection.collection import *
#import collection.collection
#from script.tools import collection
import collection
class NeuralNetwork(nn.Module):
    def __init__(self, input, hidden, layer, output):
        super().__init__()
        self.loss_history = []
        # Inputs to hidden layer linear transformation
        self.input = input
        self.hidden = hidden
        self.output = output
        self.layer = layer

        self.input_layer = nn.Linear(self.input, self.hidden)
        self.hidden_layer = []
        for i in range(0, layer):
            self.hidden_layer.push(nn.Linear(self.hidden, self.hidden))
        self.output_layer = nn.Linear(self.hidden, self.output)

        '''
        nn.init.xavier_uniform_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

        nn.init.xavier_uniform_(self.linear1.weight)
        nn.init.zeros_(self.linear1.bias)

        nn.init.xavier_uniform_(self.linear2.weight)
        nn.init.zeros_(self.linear2.bias)

        nn.init.xavier_uniform_(self.output_layer.weight)
        nn.init.zeros_(self.output_layer.bias)
        '''
        self.act = nn.Sigmoid()
    def forward(self, x):
        x = self.input_layer(x)
        x = self.act1(x)
        x = self.act2(self.hidden_layer1(x))
        x = self.act3(self.hidden_layer2(x))
        out = self.output_layer(x)
        return out

class DeepNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(DeepNet, self).__init__()

        layers = []
        layers.append(nn.Linear(input_size, hidden_size))  # 输入层
        layers.append(nn.Sigmoid())  # 第一个激活函数

        for _ in range(num_layers - 2):  # 中间的隐藏层
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.Sigmoid())

        layers.append(nn.Linear(hidden_size, output_size))  # 输出层

        self.net = nn.ModuleList(layers)

        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)

    def forward(self, x):
        for layer in self.net:
            x = layer(x)
        return x
def test(x,y,model):
    out = model(x)
from torch import nn


#自编码
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        # 编码器
        self.encoder = nn.Sequential(
            nn.Linear(19, 15),  # 输入层到隐藏层1
            nn.ReLU(True),
            nn.Linear(15, 12),   # 隐藏层1到隐藏层2
            nn.ReLU(True),
            nn.Linear(12, 8)     # 隐藏层2到编码层
        )
        # 解码器
        self.decoder = nn.Sequential(
            nn.Linear(8, 12),    # 编码层到隐藏层1
            nn.ReLU(True),
            nn.Linear(12, 15),   # 隐藏层1到隐藏层2
            nn.ReLU(True),
            nn.Linear(15, 19),  # 隐藏层2到输出层
            nn.Sigmoid()        # 使用Sigmoid激活函数确保输出值在0到1之间
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x