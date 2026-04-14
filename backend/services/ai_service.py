from dataclasses import dataclass
import json

import joblib
import numpy as np

from config.settings import settings
from models.ai_audit import AIAudit
from services.cache_service import cache_service


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

    def _drift_score(self, features: np.ndarray) -> float:
        if self.scaler is None:
            return 0.0
        return float(np.max(np.abs(features)))

    def evaluate(
        self,
        amount_eth: float,
        tx_count_last_hour: int,
        mean_interval_seconds: float,
        wallet_activity_ratio: float,
        wallet: str | None = None,
        db=None,
    ) -> RiskResult:
        cache_key = None
        if wallet:
            cache_key = f"risk:{wallet.lower()}:{int(amount_eth*10000)}:{tx_count_last_hour}"
            cached = cache_service.get_json(cache_key)
            if cached:
                return RiskResult(risk_score=float(cached["risk_score"]), anomaly_flag=bool(cached["anomaly_flag"]))

        features = np.array([[amount_eth, tx_count_last_hour, mean_interval_seconds, wallet_activity_ratio]], dtype=float)
        if self.scaler is not None:
            features = self.scaler.transform(features)
        drift = self._drift_score(features)

        if self.model is None:
            baseline = min(100.0, amount_eth * 5 + tx_count_last_hour * 3)
            result = RiskResult(risk_score=baseline, anomaly_flag=baseline >= 70)
            if cache_key:
                cache_service.set_json(
                    cache_key,
                    {"risk_score": result.risk_score, "anomaly_flag": result.anomaly_flag},
                    settings.risk_cache_ttl_seconds,
                )
            if db is not None:
                db.add(
                    AIAudit(
                        features_json=json.dumps(features.tolist()),
                        risk_score=result.risk_score,
                        anomaly_flag=result.anomaly_flag,
                        drift_score=drift,
                    )
                )
                db.commit()
            return result

        decision = self.model.decision_function(features)[0]
        pred = self.model.predict(features)[0]
        score = float(max(0.0, min(100.0, 50 - (decision * 35))))
        anomaly_flag = pred == -1 or drift > settings.ai_drift_threshold
        result = RiskResult(risk_score=score, anomaly_flag=anomaly_flag)
        if cache_key:
            cache_service.set_json(
                cache_key,
                {"risk_score": result.risk_score, "anomaly_flag": result.anomaly_flag},
                settings.risk_cache_ttl_seconds,
            )
        if db is not None:
            db.add(
                AIAudit(
                    features_json=json.dumps(features.tolist()),
                    risk_score=result.risk_score,
                    anomaly_flag=result.anomaly_flag,
                    drift_score=drift,
                )
            )
            db.commit()
        return result


ai_service = AIService()
