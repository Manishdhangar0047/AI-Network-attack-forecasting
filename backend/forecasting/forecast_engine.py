# backend/forecasting/forecast_engine.py
import random
import pandas as pd
from .mitre_mapping import MITRE_STAGES, STAGE_NUMBER
from . import real_model_interface as rmi
from models.world_model import load_processed_data, Config

USE_MOCK = False  # ab False!

_cfg = Config()
_scaled_data = None
_raw_df = None
_current_idx = 0       # demo ke liye traffic "replay" karne ke liye
_risk_history = []      # forecast_series ke liye rolling history

def _init_real_pipeline():
    global _scaled_data, _raw_df
    rmi.init_models()
    _cfg.CSV_PATH = rmi.get_world_cfg().CSV_PATH
    _scaled_data, scaler, labels, feature_names = load_processed_data(_cfg)
    _raw_df = pd.read_csv(_cfg.CSV_PATH).select_dtypes(include=["number"])

if not USE_MOCK:
    _init_real_pipeline()

def _build_stage_probabilities(current_stage, risk_score):
    probs = {str(i + 1): 0.05 for i in range(len(MITRE_STAGES))}
    probs[str(STAGE_NUMBER[current_stage])] = round(risk_score, 2)
    return probs

def _mock_stage_probabilities():
    probs = {str(i + 1): round(random.uniform(0.05, 0.3), 2) for i in range(len(MITRE_STAGES))}
    winner = random.choice(list(probs.keys()))
    probs[winner] = round(random.uniform(0.5, 0.8), 2)
    return probs

def run_forecast():
    global _current_idx

    if USE_MOCK:
        stage_probabilities = _mock_stage_probabilities()
        winner_num = max(stage_probabilities, key=stage_probabilities.get)
        predicted_stage = MITRE_STAGES[int(winner_num) - 1]
        risk_score = stage_probabilities[winner_num]
        top_features = {"Idle Mean": 0.34, "Flow IAT Std": 0.28, "Idle Max": 0.21,
                         "Fwd IAT Max": 0.11, "TotLen Fwd Pkts": 0.06}

        _risk_history.append(risk_score)
        if len(_risk_history) > 10:
            _risk_history.pop(0)
        forecast_series = list(_risk_history)

        kpis = {"threats": random.randint(1, 50), "packets": f"{random.randint(1,20)}.{random.randint(0,9)}K",
                "blocked": random.randint(10, 1500), "confidence": f"{random.randint(80,95)}%"}
    else:
        idx = _current_idx % (len(_scaled_data) - _cfg.SEQ_LEN - 1)
        recent_sequence = _scaled_data[idx: idx + _cfg.SEQ_LEN]
        actual_next = _scaled_data[idx + _cfg.SEQ_LEN]
        raw_row = _raw_df.iloc[[idx + _cfg.SEQ_LEN]]

        result = rmi.get_model_output(raw_row, recent_sequence, actual_next)
        _current_idx += 1

        predicted_stage = result["current_stage"]
        risk_score = result["risk_score"]
        top_features = result["top_features"]
        stage_probabilities = _build_stage_probabilities(predicted_stage, risk_score)

        _risk_history.append(risk_score)
        if len(_risk_history) > 10:
            _risk_history.pop(0)
        forecast_series = list(_risk_history)

        kpis = {"threats": _current_idx, "packets": f"{_current_idx * 0.1:.1f}K",
                "blocked": int(risk_score * 1000), "confidence": f"{int(risk_score*100)}%"}

    return {
        "risk_score": risk_score,
        "predicted_stage": predicted_stage,
        "stage_probabilities": stage_probabilities,
        "top_features": top_features,
        "forecast_series": forecast_series,
        "kpis": kpis
    }