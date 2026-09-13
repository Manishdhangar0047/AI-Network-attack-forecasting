# backend/forecasting/risk_combiner.py
import numpy as np

# Member 2 ke actual stats (12,928 rows, 79 features, train+val combined)
ANOMALY_MEAN = 0.8943
ANOMALY_STD = 2.0611
ANOMALY_P95 = 3.1410   # isse "max normal-ish" error maan rahe hain, isse upar clip karenge 1.0 pe

def normalize_anomaly(error: float) -> float:
    """Raw MSE -> 0-1 range. 95th percentile ko upper bound maan ke simple min-max clip."""
    return float(min(error / ANOMALY_P95, 1.0))

def combine_risk(baseline_proba: float, anomaly_error: float,
                  w_baseline: float = 0.7, w_anomaly: float = 0.3) -> float:
    anomaly_norm = normalize_anomaly(anomaly_error)
    return round(w_baseline * baseline_proba + w_anomaly * anomaly_norm, 2)