import torch
from pathlib import Path
from model_train import MetricsModelV1
from backend.train_test_split import X_train, X_test, y_train, y_test

device = "cuda" if torch.cuda.is_available() else "cpu"

metrics_model = MetricsModelV1(input_features = 18,
                               output_features = 1,
                               hidden_units = 18).to(device)

# Train model
epochs = 2000

loss_fn = torch.nn.L1Loss()
optimizer = torch.optim.Adam(metrics_model.parameters(), lr=1e-4)

for epoch in range(epochs):
  metrics_model.train()

  y_logits = metrics_model(X_train).squeeze()
  loss = loss_fn(y_logits, y_train)

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  metrics_model.eval()
  with torch.inference_mode():
    y_test_logits = metrics_model(X_test).squeeze()
    test_loss = loss_fn(y_test_logits, y_test)

  if epoch % 10 == 0:
    print(f"Epoch: {epoch} | Loss: {loss * 100:.5f} | Test loss: {test_loss * 100:.5f}")
