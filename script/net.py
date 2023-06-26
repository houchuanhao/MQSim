import torch.nn as nn
#from collection.collection import *
#import collection.collection
from script.tools import collection

class net(nn.Module):
    def __init__(self, input, hidden, width, output):
        super().__init__()
        self.loss_history = []
        # Inputs to hidden layer linear transformation
        self.input = input
        self.hidden = hidden
        print(self.hidden)
        self.output = output
        self.width = width
        self.input_layer = nn.Linear(self.input, self.width)
        self.hidden_layer1 = nn.Linear(self.width, self.width)
        self.hidden_layer2 = nn.Linear(self.width, self.width)
        self.output_layer = nn.Linear(self.width, self.output)

        # Define sigmoid activation and softma1x output
        self.act1 = nn.Sigmoid()
        self.act2 = nn.Sigmoid()
        self.act3 = nn.Sigmoid()
    def forward(self, x):
        x = self.input_layer(x)
        x = self.act1(x)
        x = self.act2(self.hidden_layer1(x))
        x = self.act3(self.hidden_layer2(x))
        out = self.output_layer(x)
        return out