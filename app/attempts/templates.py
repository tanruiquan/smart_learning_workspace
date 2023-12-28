import torch
import torch.nn as nn


class TemplateMLP(nn.Module):

    def __init__(self, input_size, output_size, hidden_sizes=[], activation=nn.ReLU(), dropout=0.0, batch_norm=False):
        """
        Parameters
        ----------
        input_size : int
            the size of the input features
        output_size : int
            the size of the output layer
        hidden_sizes : List(int)
            a list of hidden layer sizes
        activation : nn.Module, optional
            the activation function to be applied between hidden layers (default is nn.ReLu())
        dropout : float, optional
            the dropout rate, set to 0.0 to disable dropout (default is 0.0)
        batch_norm : bool, optional
            use batch normalisation between hidden layers (default is False)
        """
        super().__init__()

        layers = []
        layer_sizes = [input_size] + hidden_sizes + [output_size]
        for i in range(len(layer_sizes) - 2):
            layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))

            if batch_norm:
                layers.append(nn.BatchNorm1d(layer_sizes[i + 1]))

            layers.append(activation)

            if dropout > 0:
                layers.append(nn.Dropout(p=dropout))

        # Output layer
        layers.append(nn.Linear(layer_sizes[-2], layer_sizes[-1]))
        layers.append(nn.LogSoftmax(dim=1))

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class TemplateRNN(nn.Module):
    def __init__(self, vocab_size, embed_size, rnn_cell, rnn_hidden_size, output_size, rnn_num_layers=1, rnn_bidirectional=False, rnn_dropout=0.0, dot_attention=False, linear_hidden_size=[], linear_dropout=0.0):
        super().__init__()

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embed_size)

        # RNN layers
        self.rnn = self.get_rnn(rnn_cell, embed_size, rnn_hidden_size,
                                rnn_num_layers, rnn_bidirectional, rnn_dropout)

        # Attention layer if dot_attention is True
        self.attention = self.get_attention(dot_attention, rnn_hidden_size)

        # Linear layers
        self.linear_layers = self.get_linear_layers(
            rnn_hidden_size, linear_hidden_size, linear_dropout, output_size)

    def get_rnn(self, rnn_cell, input_size, hidden_size, num_layers, bidirectional, dropout):
        if rnn_cell == "LSTM":
            return nn.LSTM(input_size, hidden_size, num_layers, bidirectional=bidirectional, dropout=dropout, batch_first=True)
        elif rnn_cell == "GRU":
            return nn.GRU(input_size, hidden_size, num_layers, bidirectional=bidirectional, dropout=dropout, batch_first=True)
        else:
            return nn.RNN(input_size, hidden_size, num_layers, bidirectional=bidirectional, dropout=dropout, batch_first=True)

    def get_attention(self, dot_attention, hidden_size):
        if dot_attention:
            return nn.Linear(hidden_size, 1)

    def get_linear_layers(self, input_size, hidden_sizes, dropout, output_size, activation=nn.ReLU()):
        layers = []
        prev_size = input_size

        for size in hidden_sizes:
            layers.append(nn.Linear(prev_size, size))
            layers.append(activation)
            layers.append(nn.Dropout(dropout))
            prev_size = size

        layers.append(nn.Linear(prev_size, output_size))
        layers.append(nn.LogSoftmax(dim=1))

        return nn.Sequential(*layers)

    def forward(self, x):
        # Embedding layer
        embedded = self.embedding(x)

        # RNN layers
        rnn_output, _ = self.rnn(embedded)

        # Attention if enabled
        if self.attention:
            attention_weights = torch.softmax(
                self.attention(rnn_output), dim=1)
            rnn_output = rnn_output * attention_weights

        # Linear layers
        # Assuming you want the output at the last time step
        output = self.linear_layers(rnn_output[:, -1, :])
        return output
