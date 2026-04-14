from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def generate_synthetic_data(samples: int = 5000) -> np.ndarray:
    rng = np.random.default_rng(42)
    amount = rng.gamma(shape=2.0, scale=0.5, size=samples)
    tx_frequency = rng.poisson(lam=3, size=samples)
    time_interval = rng.normal(loc=2400, scale=900, size=samples).clip(10, 86400)
    wallet_activity = rng.uniform(0.05, 0.95, size=samples)
    return np.column_stack([amount, tx_frequency, time_interval, wallet_activity])


def train() -> None:
    data = generate_synthetic_data()
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)
    model = IsolationForest(contamination=0.05, random_state=42, n_estimators=200)
    model.fit(x_scaled)

    out_dir = Path(__file__).parent / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_dir / "isolation_forest.joblib")
    joblib.dump(scaler, out_dir / "scaler.joblib")
    print(f"Saved model artifacts in {out_dir}")


if __name__ == "__main__":
    train()
