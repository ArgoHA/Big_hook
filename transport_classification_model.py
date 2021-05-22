#transport_classification_model.py
from torch import nn
import torch
from torch.utils.data import DataLoader, Dataset, TensorDataset, random_split

'''
BiLSTM + CNN модель, обучение которой позволит дополнительно выделять сигнатуру транспорта (делить временной ряд сигнала на фрагменты, где был транспорт)
Аналогичная модель с большИм количеством классов позволит классифицировать типы транспорт (легковой, автобус, грузовой, газель и т.п.)
'''

#Model CNN_BiLSTM - try BiLSMCRF or just BiLSTM
class CNN_BiLSTM(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=10, in_out_dim=4000, n_classes=2):
        super(CNN_BiLSTM, self).__init__()
        self.hidden_size = hidden_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, bidirectional = True) #output 400 x 2 x hidden_dim
        
        self.linear = nn.Sequential(nn.Linear(hidden_dim*in_out_dim*2, hidden_dim*in_out_dim), nn.ReLU()) 
        
        #kernel was 4 instead of (5,1)
        self.conv_layer = nn.Sequential(nn.Conv2d(1, 32, (5,1), 1, (2,1)),
                                       nn.ReLU(),
                                       nn.Conv2d(32, 64, (5,1), 1, (2,1)),
                                       nn.ReLU(),
                                       nn.MaxPool2d((1,5), 1, (0,0)),
                                       nn.ReLU())
        
        self.linear_out = nn.Linear(64, n_classes) #(b,4000,1orX) -> (b,4000,n_classes)

    def forward(self, X, hidden):
        #print(X)
        output_lstm, _ = self.lstm(X) #([1, 4000, 2])
        output_lstm = output_lstm.view(X.shape[0], -1) #([1, 8000])
        output1 = self.linear(output_lstm) #([1, 4000])
        output1 = output1.view(X.shape[0], 1, X.shape[1], 1) #([1, 1, 4000, 1])
        output_cnn = self.conv_layer(output1) #([1, 64, 4000, 1])
        output_cnn = output_cnn.view(X.shape[0], X.shape[1], 64) #([1, 4000, 64])
        output = self.linear_out(output_cnn) #([1, 4000, 6])
        return output