# backend/forecasting/mitre_mapping.py

MITRE_STAGES = [
    "Reconnaissance",
    "Initial Access",
    "Lateral Movement",
    "Command & Control",
    "Exfiltration"
]

STAGE_INDEX = {stage: i for i, stage in enumerate(MITRE_STAGES)}
STAGE_NUMBER = {stage: i + 1 for i, stage in enumerate(MITRE_STAGES)}  # frontend wants "1"-"5"

# Exact labels from network_traffic_sample.csv (df["Label"].value_counts())
CICIDS_LABEL_TO_STAGE = {
    "Benign": None,

    # Initial Access — brute force / injection style entry attempts
    "FTP-BruteForce": "Initial Access",
    "SSH-Bruteforce": "Initial Access",
    "Brute Force -Web": "Initial Access",
    "Brute Force -XSS": "Initial Access",
    "SQL Injection": "Initial Access",

    # Lateral Movement
    "Infilteration": "Lateral Movement",   # note: dataset spells it "Infilteration", not "Infiltration"

    # Command & Control
    "Bot": "Command & Control",

    # DoS/DDoS -> mapped to Command & Control as nearest available stage (ASSUMPTION — confirm with team/mentor,
    # since MITRE's real category for these is "Impact", which isn't one of our 5 defined stages)
    "DDOS attack-LOIC-UDP": "Command & Control",
    "DDoS attacks-LOIC-HTTP": "Command & Control",
    "DDOS attack-HOIC": "Command & Control",
    "DoS attacks-GoldenEye": "Command & Control",
    "DoS attacks-Hulk": "Command & Control",
    "DoS attacks-SlowHTTPTest": "Command & Control",
    "DoS attacks-Slowloris": "Command & Control",
}

def get_next_stage(current_stage: str):
    idx = STAGE_INDEX.get(current_stage)
    if idx is None or idx == len(MITRE_STAGES) - 1:
        return None
    return MITRE_STAGES[idx + 1]

def label_to_stage(label: str):
    """Baseline model ka predicted attack label -> MITRE stage."""
    return CICIDS_LABEL_TO_STAGE.get(label)