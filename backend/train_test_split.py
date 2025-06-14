from sklearn.model_selection import train_test_split
import pandas as pd
import torch

data_frame = pd.read_csv('./model_files/synthetic_data.csv')

# Convert df to numpy array
raw_X = data_frame.drop(columns=["score"])
raw_y = data_frame["score"]

raw_X = raw_X.to_numpy()
raw_y = raw_y.to_numpy()


# Convert the numpy arrays to tensors
X = torch.from_numpy(raw_X).type(torch.float32)
y = torch.from_numpy(raw_y).type(torch.float32)

# Create test and split data
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size = 0.2,
                                                    random_state = 42)

# Compute normalization parameters on full training set [-1, 1]
# Equation -> X_norm = (X - mean_of_data) / standard_deviation
X_mean = X.mean(dim=0, keepdim=True)
X_std = X.std(dim=0, keepdim=True)

X_train = (X_train - X_mean) / (X_std + 1e-8)
X_test = (X_test - X_mean) / (X_std + 1e-8)  


y_mean = y.mean(dim=0, keepdim=True)
y_std = y.std(dim=0, keepdim=True)

y_train = (y_train - y_mean) / (y_std + 1e-8)
y_test = (y_test - y_mean) / (y_std + 1e-8)