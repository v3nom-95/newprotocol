from dataclasses import dataclass

import joblib
import numpy as np


@dataclass
class InferenceOutput:
    risk_score: float
    anomaly_flag: bool


class QAIRiskModel:
    def __init__(self, model_path: str, scaler_path: str):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, amount_eth: float, tx_frequency: float, time_interval: float, wallet_activity: float) -> InferenceOutput:
        x = np.array([[amount_eth, tx_frequency, time_interval, wallet_activity]], dtype=float)
        x_scaled = self.scaler.transform(x)
        pred = self.model.predict(x_scaled)[0]
        decision = self.model.decision_function(x_scaled)[0]
        risk_score = float(max(0.0, min(100.0, 50 - (decision * 35))))
        return InferenceOutput(risk_score=risk_score, anomaly_flag=pred == -1)
