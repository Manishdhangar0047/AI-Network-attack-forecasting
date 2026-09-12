import os
import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from world_model import WorldModel, Config

dataset_path = os.path.join("..", "..", "sample_dataset", "network_traffic_sample.csv")
df = pd.read_csv(dataset_path)

df["Label_binary"] = df["Label"].apply(lambda x: 0 if str(x).strip() == "Benign" else 1)

drop_cols = [c for c in ["Timestamp", "Flow ID", "Src IP", "Dst IP", "Label", "Label_binary"] if c in df.columns]
X_raw = df.drop(columns=drop_cols).select_dtypes(include=["number"])
X_raw = X_raw.replace([np.inf, -np.inf], 0).fillna(0)
y = df["Label_binary"].values

X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.2, random_state=42)

baseline = LogisticRegression(max_iter=1000)
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_test)

print("===== BASELINE MODEL (Logistic Regression) =====")
print("Accuracy :", accuracy_score(y_test, baseline_pred))
print("Precision:", precision_score(y_test, baseline_pred))
print("Recall   :", recall_score(y_test, baseline_pred))
print("F1 Score :", f1_score(y_test, baseline_pred))

cfg = Config()
scaler_data = np.load("scaler.npy", allow_pickle=True).item()
mean = scaler_data["mean"]
scale = scaler_data["scale"]

scaled_data = (X_raw.values - mean) / scale

model = WorldModel(
    num_features=scaled_data.shape[1],
    hidden_size=cfg.HIDDEN_SIZE,
    num_layers=cfg.NUM_LAYERS,
    pred_len=cfg.PRED_LEN,
    dropout=cfg.DROPOUT,
)
model.load_state_dict(torch.load("world_model.pt", map_location="cpu"))
model.eval()

seq_len = cfg.SEQ_LEN
errors = []
seq_labels = []

with torch.no_grad():
    for i in range(len(scaled_data) - seq_len - 1):
        x = torch.tensor(scaled_data[i:i + seq_len], dtype=torch.float32).unsqueeze(0)
        true_next = scaled_data[i + seq_len]
        pred_next = model(x).squeeze(0).squeeze(0).numpy()
        error = np.mean((pred_next - true_next) ** 2)
        errors.append(error)
        seq_labels.append(y[i + seq_len])

errors = np.array(errors)
seq_labels = np.array(seq_labels)

threshold = np.percentile(errors, 70)
world_pred = (errors > threshold).astype(int)

print("")
print("===== WORLD MODEL (LSTM, error-based anomaly detection) =====")
print("Accuracy :", accuracy_score(seq_labels, world_pred))
print("Precision:", precision_score(seq_labels, world_pred))
print("Recall   :", recall_score(seq_labels, world_pred))
print("F1 Score :", f1_score(seq_labels, world_pred))
