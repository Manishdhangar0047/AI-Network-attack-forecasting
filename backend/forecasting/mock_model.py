import random
from .mitre_mapping import MITRE_STAGES

def get_mock_model_output():
    """
    Member 2/3 ka LSTM/baseline model abhi ready nahi hai.
    Ye function unki jagah dummy realistic output deta hai
    taaki forecast_engine test ho sake.
    """
    current_stage = random.choice(MITRE_STAGES)
    probs = {stage: round(random.uniform(0.05, 0.3), 2) for stage in MITRE_STAGES}
    return {
        "current_stage": current_stage,
        "stage_probabilities": probs,
        "flow_id": "mock-flow-001"
    }