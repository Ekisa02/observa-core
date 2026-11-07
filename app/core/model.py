import os
import torch
import torch.nn as nn
from typing import Optional

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_FILE = os.path.join(MODEL_DIR, "autoencoder.pt")


class Autoencoder(nn.Module):
    def __init__(self, input_dim: int = 8, latent_dim: int = 4):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, max(latent_dim * 2, 4)),
            nn.ReLU(),
            nn.Linear(max(latent_dim * 2, 4), latent_dim),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, max(latent_dim * 2, 4)),
            nn.ReLU(),
            nn.Linear(max(latent_dim * 2, 4), input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        xrec = self.decoder(z)
        return xrec


class ModelWrapper:
    """Simple wrapper to save/load a CPU model and compute reconstruction errors."""

    def __init__(self, input_dim: int = 8, latent_dim: int = 4, model_file: Optional[str] = None):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.model_file = model_file or MODEL_FILE
        self.device = torch.device("cpu")
        self.model = Autoencoder(input_dim=self.input_dim, latent_dim=self.latent_dim)
        self.model.to(self.device)

    def save(self, path: Optional[str] = None):
        path = path or self.model_file
        torch.save({
            "input_dim": self.input_dim,
            "latent_dim": self.latent_dim,
            "state_dict": self.model.state_dict(),
        }, path)

    def load(self, path: Optional[str] = None):
        path = path or self.model_file
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        checkpoint = torch.load(path, map_location=self.device)
        self.input_dim = checkpoint.get("input_dim", self.input_dim)
        self.latent_dim = checkpoint.get("latent_dim", self.latent_dim)
        self.model = Autoencoder(input_dim=self.input_dim, latent_dim=self.latent_dim)
        self.model.load_state_dict(checkpoint["state_dict"])
        self.model.to(self.device)

    def score(self, vector: list) -> float:
        import numpy as np

        arr = torch.tensor(vector, dtype=torch.float32, device=self.device)
        if arr.dim() == 1:
            arr = arr.unsqueeze(0)
        with torch.no_grad():
            rec = self.model(arr)
            mse = torch.mean((arr - rec) ** 2, dim=1)
        return float(mse.item())


# helper to ensure a model exists
def ensure_model_exists(path: Optional[str] = None, input_dim: int = 8):
    path = path or MODEL_FILE
    if not os.path.exists(path):
        wrapper = ModelWrapper(input_dim=input_dim)
        # Initialize with random weights (placeholder for an actual training pipeline)
        wrapper.save(path)
    return path
