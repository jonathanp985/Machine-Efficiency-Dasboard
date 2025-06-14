import torch
from torch import nn

class MetricsModelV1(nn.Module):
  def __init__(self, input_features, output_features, hidden_units):
    super().__init__()
    self.layers = nn.Sequential(
        nn.Linear(in_features = input_features, out_features = hidden_units),
        nn.Linear(in_features = hidden_units, out_features = hidden_units),
        nn.Linear(in_features = hidden_units, out_features = hidden_units),
        nn.Linear(in_features = hidden_units, out_features = output_features)
    )
  def forward(self, x: torch.Tensor) -> torch.Tensor:
    return self.layers(x)
