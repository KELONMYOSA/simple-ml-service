import __main__

import torch
import torch.nn as nn


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.relu = nn.ReLU()
        self.layers = []
        for _ in range(num_layers):
            self.layers.append(nn.Linear(hidden_size, hidden_size))
            self.layers.append(nn.BatchNorm1d(hidden_size))
            self.layers.append(nn.ReLU())
        self.layers = nn.Sequential(*self.layers)
        self.fc2 = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.layers(x)
        x = self.fc2(x)
        return x


setattr(__main__, "NeuralNetwork", NeuralNetwork)


def load_nn_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model_nn = torch.load("models/NN.pt", map_location=device)
    model_nn.eval()

    return model_nn


def nn_predict(model_nn, data):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    tensor_data = torch.from_numpy(data).to(device, dtype=torch.float32)
    with torch.no_grad():
        result = model_nn(tensor_data).item()

    binary_result = 1 if result > 0.5 else 0

    return {"score": binary_result}
