import torch
import torch.nn as nn

class CarNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(5, 32),
            nn.ReLU(),

            nn.Linear(32, 32),
            nn.ReLU(),

            nn.Linear(32, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.network(x)