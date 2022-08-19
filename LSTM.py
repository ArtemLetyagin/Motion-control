import torch.nn as nn
import torch
from torch.autograd import Variable 
from torch.utils.data import Dataset
import numpy as np

class Model(nn.Module):
    def __init__(self, num_layers, hidden_size, num_motions):
        super(Model, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=10, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.l1 = nn.Linear(hidden_size, num_motions)
        self.relu = nn.ReLU()
    def forward(self, x):
        #out = self.CNN(x).view(-1, 1, 180)

        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #internal state
        
        out, (hn, cn) = self.lstm(x, (h_0, c_0))
        hn = hn.view(-1, self.hidden_size)
        return self.l1(hn)

class FingerDataset(Dataset):
    def __init__(self, paths):
        arrays = []
        for i in range(len(paths)):
            arrays.append(np.load(paths[i]))
        
        self.data = np.concatenate(arrays)
        self.labels = []
        for i in range(len(paths)):
            self.labels+=[i]*len(arrays[i])
        
    def __getitem__(self, index):
        return self.data[index], self.labels[index]
    
    def __len__(self):
        return len(self.data)