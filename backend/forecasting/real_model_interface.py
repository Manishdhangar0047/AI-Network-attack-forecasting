# backend/forecasting/real_model_interface.py
import os
import joblib
import numpy as np
import pandas as pd

from models.world_model import load_trained_model, forecast, compute_anomaly_score, Config
from .mitre_mapping import label_to_stage
from .risk_combiner import combine_risk

FORECASTING_DIR = os.path.dirname(os.path.abspath(__file__))          # backend/forecasting/
BACKEND_DIR = os.path.dirname(FORECASTING_DIR)                         # backend/
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)                            # project root

TOP_FEATURES = {
    "Flow Duration": 0.32, "Fwd IAT Tot": 0.24, "Bwd IAT Tot": 0.19,
    "Bwd IAT Max": 0.14, "Fwd IAT Max": 0.11
}

_baseline_model = None
_label_encoder = None
_feature_columns = None
_world_model = None
_world_cfg = None

def init_models():
    global _baseline_model, _label_encoder, _feature_columns, _world_model, _world_cfg
    _baseline_model = joblib.load(os.path.join(BACKEND_DIR, "model.pkl"))
    _label_encoder = joblib.load(os.path.join(BACKEND_DIR, "label_encoder.pkl"))
    _feature_columns = joblib.load(os.path.join(BACKEND_DIR, "feature_columns.pkl"))

    _world_cfg = Config()
    # Hardcoded relative paths ko absolute bana rahe hain, taaki kahin se bhi run karo, sahi chale
    _world_cfg.MODEL_SAVE_PATH = os.path.join(BACKEND_DIR, "models", "world_model.pt")
    _world_cfg.SCALER_SAVE_PATH = os.path.join(BACKEND_DIR, "models", "scaler.npy")
    _world_cfg.CSV_PATH = os.path.join(PROJECT_ROOT, "sample_dataset", "network_traffic_sample.csv")

    _world_model = load_trained_model(num_features=len(_feature_columns), config=_world_cfg)

def predict_baseline(flow_features_df: pd.DataFrame):
    input_df = flow_features_df[_feature_columns].replace([np.inf, -np.inf], 0).fillna(0)
    proba = _baseline_model.predict_proba(input_df)[0]
    classes = _label_encoder.inverse_transform(_baseline_model.classes_)
    pred_idx = proba.argmax()
    predicted_label = classes[pred_idx]
    probability = float(proba[pred_idx])
    return predicted_label, probability

def get_model_output(flow_features_df: pd.DataFrame, recent_sequence_scaled: np.ndarray, actual_next_scaled: np.ndarray):
    attack_label, attack_proba = predict_baseline(flow_features_df)
    stage = label_to_stage(attack_label) or "Reconnaissance"
    anomaly_error = compute_anomaly_score(_world_model, recent_sequence_scaled, actual_next_scaled, _world_cfg)
    final_risk = combine_risk(attack_proba, anomaly_error)
    return {"current_stage": stage, "risk_score": final_risk, "top_features": TOP_FEATURES, "attack_label": attack_label}

def get_world_cfg():
    return _world_cfg