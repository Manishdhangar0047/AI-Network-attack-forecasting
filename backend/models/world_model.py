"""
world_model.py
Member 2 - ML Engineer (World Model / LSTM)
SIH26153 - AI based Network Attack Forecasting from Network Traffic Data

Data source: sample_dataset/network_traffic_sample.csv  (from Member 1's data_pipeline)

CSV mein columns:
    - Non-feature / identifier columns (DROP kiye jaate hain):
        Timestamp, Flow ID, Src IP, Dst IP
    - Label column (attack type, abhi world model ke liye use nahi ho raha,
      future mein classification/explainability ke liye Member 3 use karega):
        Label
    - Baaki sab numeric feature columns (Flow Duration, Tot Fwd Pkts,
      Flow Byts/s, etc.) -> ye LSTM ka input banenge.
"""

import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# -----------------------------
# 1. Config
# -----------------------------
class Config:
    CSV_PATH = "sample_dataset/network_traffic_sample.csv"

    # Ye columns feature ke liye nahi use honge
    DROP_COLUMNS = ["Timestamp", "Flow ID", "Src IP", "Dst IP"]
    LABEL_COLUMN = "Label"

    SEQ_LEN = 15            # kitne past flows dekh kar predict karna hai
    PRED_LEN = 1             # kitne future flows predict karne hain
    HIDDEN_SIZE = 64
    NUM_LAYERS = 2
    DROPOUT = 0.2
    BATCH_SIZE = 64
    EPOCHS =5
    LEARNING_RATE = 1e-3
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    MODEL_SAVE_PATH = "backend/models/world_model.pt"
    SCALER_SAVE_PATH = "backend/models/scaler.npy"


# -----------------------------
# 2. Data loading + cleaning
# -----------------------------
def load_processed_data(config: Config = Config()):
    """
    CSV load karta hai, identifier columns drop karta hai, Label ko alag
    rakhta hai (abhi world model use nahi karega), aur numeric features
    ko scale karta hai.
    """
    df = pd.read_csv(config.CSV_PATH)

    drop_cols = [c for c in config.DROP_COLUMNS if c in df.columns]
    df = df.drop(columns=drop_cols)

    labels = None
    if config.LABEL_COLUMN in df.columns:
        labels = df[config.LABEL_COLUMN]
        df = df.drop(columns=[config.LABEL_COLUMN])

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    df = df.select_dtypes(include=[np.number])

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df.values)

    print(f"Loaded data shape: {scaled.shape}  (rows, features)")
    print(f"Feature columns used ({df.shape[1]}): {list(df.columns)[:10]} ...")

    return scaled, scaler, labels, df.columns.tolist()


# -----------------------------
# 3. Dataset class
# -----------------------------
class TrafficSequenceDataset(Dataset):
    def __init__(self, data: np.ndarray, seq_len: int, pred_len: int = 1):
        self.data = data
        self.seq_len = seq_len
        self.pred_len = pred_len

    def __len__(self):
        return max(0, len(self.data) - self.seq_len - self.pred_len + 1)

    def __getitem__(self, idx):
        x = self.data[idx: idx + self.seq_len]
        y = self.data[idx + self.seq_len: idx + self.seq_len + self.pred_len]
        return (
            torch.tensor(x, dtype=torch.float32),
            torch.tensor(y, dtype=torch.float32),
        )


# -----------------------------
# 4. LSTM World Model
# -----------------------------
class WorldModel(nn.Module):
    def __init__(self, num_features, hidden_size=64, num_layers=2, pred_len=1, dropout=0.2):
        super().__init__()
        self.num_features = num_features
        self.pred_len = pred_len

        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.fc = nn.Linear(hidden_size, num_features * pred_len)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        last_hidden = out[:, -1, :]
        pred = self.fc(last_hidden)
        pred = pred.view(-1, self.pred_len, self.num_features)
        return pred


# -----------------------------
# 5. Training loop
# -----------------------------
def train_model(config: Config = Config()):
    data, scaler, labels, feature_names = load_processed_data(config)

    train_data, val_data = train_test_split(data, test_size=0.2, shuffle=False)

    train_ds = TrafficSequenceDataset(train_data, config.SEQ_LEN, config.PRED_LEN)
    val_ds = TrafficSequenceDataset(val_data, config.SEQ_LEN, config.PRED_LEN)

    train_loader = DataLoader(train_ds, batch_size=config.BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=config.BATCH_SIZE, shuffle=False)

    num_features = data.shape[1]
    model = WorldModel(
        num_features=num_features,
        hidden_size=config.HIDDEN_SIZE,
        num_layers=config.NUM_LAYERS,
        pred_len=config.PRED_LEN,
        dropout=config.DROPOUT,
    ).to(config.DEVICE)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    os.makedirs(os.path.dirname(config.MODEL_SAVE_PATH), exist_ok=True)

    best_val_loss = float("inf")

    for epoch in range(1, config.EPOCHS + 1):
        model.train()
        train_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(config.DEVICE), y.to(config.DEVICE)
            optimizer.zero_grad()
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x.size(0)
        train_loss /= max(1, len(train_ds))

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(config.DEVICE), y.to(config.DEVICE)
                pred = model(x)
                loss = criterion(pred, y)
                val_loss += loss.item() * x.size(0)
        val_loss /= max(1, len(val_ds))

        print(f"Epoch {epoch}/{config.EPOCHS} | Train Loss: {train_loss:.5f} | Val Loss: {val_loss:.5f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), config.MODEL_SAVE_PATH)
            np.save(config.SCALER_SAVE_PATH, {
                "mean": scaler.mean_,
                "scale": scaler.scale_,
                "feature_names": feature_names,
            })

    print(f"Training complete. Best model saved to {config.MODEL_SAVE_PATH}")
    return model, scaler


# -----------------------------
# 6. Inference helpers (Member 4 backend isko call karega)
# -----------------------------
def load_trained_model(num_features: int, config: Config = Config()):
    model = WorldModel(
        num_features=num_features,
        hidden_size=config.HIDDEN_SIZE,
        num_layers=config.NUM_LAYERS,
        pred_len=config.PRED_LEN,
        dropout=config.DROPOUT,
    )
    model.load_state_dict(torch.load(config.MODEL_SAVE_PATH, map_location=config.DEVICE))
    model.to(config.DEVICE)
    model.eval()
    return model


def forecast(model, recent_sequence: np.ndarray, config: Config = Config()):
    """
    recent_sequence: (seq_len, num_features) numpy array, already scaled
    returns: (pred_len, num_features) numpy array -> forecasted future state
    """
    model.eval()
    with torch.no_grad():
        x = torch.tensor(recent_sequence, dtype=torch.float32).unsqueeze(0).to(config.DEVICE)
        pred = model(x)
    return pred.squeeze(0).cpu().numpy()

# -----------------------------
# 6b. Anomaly score (Member 4 ke liye - risk_score ka secondary signal)
# -----------------------------
def compute_anomaly_score(model, recent_sequence: np.ndarray, actual_next: np.ndarray, config: Config = Config()):
    """
    ...
    """
    predicted = forecast(model, recent_sequence, config)
    predicted_next = predicted[0]
    error = np.mean((predicted_next - actual_next) ** 2)
    return float(error)


# -----------------------------
# 7. Script entry point
# -----------------------------
if __name__ == "__main__":
    cfg = Config()
    if os.path.exists(cfg.CSV_PATH):
        train_model(cfg)
    else:
        print(f"'{cfg.CSV_PATH}' nahi mila. Path check karo (project root se run karo).")
