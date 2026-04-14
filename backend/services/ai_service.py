from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

import joblib
import numpy as np

from config.settings import settings


@dataclass
class RiskResult:
    risk_score: float
    anomaly_flag: bool


class AIService:
    def __init__(self) -> None:
        self.model = None
        self.scaler = None
        self._load()

    def _load(self) -> None:
        try:
            self.model = joblib.load(settings.model_path)
            self.scaler = joblib.load(settings.feature_scaler_path)
        except Exception:
            self.model = None
            self.scaler = None

    def evaluate(self, amount_eth: float, tx_count_last_hour: int, mean_interval_seconds: float, wallet_activity_ratio: float) -> RiskResult:
        features = np.array([[amount_eth, tx_count_last_hour, mean_interval_seconds, wallet_activity_ratio]], dtype=float)
        if self.scaler is not None:
            features = self.scaler.transform(features)

        if self.model is None:
            baseline = min(100.0, amount_eth * 5 + tx_count_last_hour * 3)
            return RiskResult(risk_score=baseline, anomaly_flag=baseline >= 70)

        decision = self.model.decision_function(features)[0]
        pred = self.model.predict(features)[0]
        score = float(max(0.0, min(100.0, 50 - (decision * 35))))
        return RiskResult(risk_score=score, anomaly_flag=pred == -1)


ai_service = AIService()
