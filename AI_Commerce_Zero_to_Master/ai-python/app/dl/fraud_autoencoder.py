"""Optional educational autoencoder for anomaly detection."""
import torch
from torch import nn

class FraudAutoencoder(nn.Module):
    def __init__(self, feature_count: int = 8):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(feature_count, 16), nn.ReLU(), nn.Linear(16, 4))
        self.decoder = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, feature_count))

    def forward(self, x):
        return self.decoder(self.encoder(x))

if __name__ == "__main__":
    model = FraudAutoencoder()
    batch = torch.rand(16, 8)
    reconstruction = model(batch)
    error = ((batch - reconstruction) ** 2).mean(dim=1)
    print("reconstruction error:", error[:5])
