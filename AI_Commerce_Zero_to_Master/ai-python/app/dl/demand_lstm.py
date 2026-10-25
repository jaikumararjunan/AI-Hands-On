"""Optional educational LSTM for demand forecasting; demonstrates sequence modeling, not a tuned production model."""
import torch
from torch import nn

class DemandLSTM(nn.Module):
    def __init__(self, input_size: int = 1, hidden_size: int = 32):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, sequence):
        output, _ = self.lstm(sequence)
        return self.head(output[:, -1, :])

if __name__ == "__main__":
    model = DemandLSTM()
    sample = torch.rand(4, 30, 1)  # batch=4, 30-day history
    print(model(sample).shape)
