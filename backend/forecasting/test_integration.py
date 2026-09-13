# backend/forecasting/test_integration.py
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))  # project root

import numpy as np
import pandas as pd
from backend.forecasting import real_model_interface as rmi
from backend.models.world_model import load_processed_data, Config

# Models load karo (ek hi baar)
rmi.init_models()

# CSV se ek sample sequence lete hain testing ke liye
cfg = Config()
scaled_data, scaler, labels, feature_names = load_processed_data(cfg)

idx = 100  # koi bhi valid index (seq_len=15 se aage)
recent_sequence = scaled_data[idx : idx + cfg.SEQ_LEN]
actual_next = scaled_data[idx + cfg.SEQ_LEN]

# Baseline ke liye raw (unscaled) row chahiye — CSV se seedha
df = pd.read_csv(cfg.CSV_PATH)
raw_row = df.select_dtypes(include=["number"]).iloc[[idx + cfg.SEQ_LEN]]

result = rmi.get_model_output(raw_row, recent_sequence, actual_next)
print(result)