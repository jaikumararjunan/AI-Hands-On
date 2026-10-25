"""Optional PyTorch example: two-tower recommendation model.
Install requirements-dl.txt before running.
"""
import torch
from torch import nn

class TwoTowerModel(nn.Module):
    def __init__(self, num_users: int, num_products: int, embedding_dim: int = 32):
        super().__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.product_embedding = nn.Embedding(num_products, embedding_dim)

    def forward(self, user_ids, product_ids):
        user_vec = self.user_embedding(user_ids)
        product_vec = self.product_embedding(product_ids)
        user_vec = nn.functional.normalize(user_vec, dim=-1)
        product_vec = nn.functional.normalize(product_vec, dim=-1)
        return (user_vec * product_vec).sum(dim=-1)

if __name__ == "__main__":
    model = TwoTowerModel(num_users=1000, num_products=5000)
    users = torch.tensor([1, 2, 3])
    products = torch.tensor([10, 20, 30])
    print("scores:", model(users, products))
