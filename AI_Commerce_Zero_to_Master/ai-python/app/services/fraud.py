import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class FraudService:
    def __init__(self):
        rng = np.random.default_rng(42)
        n = 2500
        baseline = pd.DataFrame({
            "amount": rng.lognormal(mean=9.5, sigma=0.7, size=n),
            "quantity": rng.integers(1, 6, size=n),
            "discount_pct": rng.uniform(0, 0.25, size=n),
            "account_age_days": rng.integers(10, 2500, size=n),
            "orders_last_hour": rng.poisson(0.4, size=n) + 1,
        })
        self.columns = list(baseline.columns)
        self.model = Pipeline([
            ("scale", StandardScaler()),
            ("isolation", IsolationForest(contamination=0.02, random_state=42)),
        ])
        self.model.fit(baseline[self.columns])

    def score(self, payload: dict):
        row = pd.DataFrame([{c: payload[c] for c in self.columns}])
        prediction = int(self.model.predict(row)[0])
        decision = float(self.model.decision_function(row)[0])
        risk = min(1.0, max(0.0, 0.5 - decision * 2.0))
        return {
            "classification": "REVIEW" if prediction == -1 else "NORMAL",
            "risk_score": round(risk, 4),
            "model": "IsolationForest demo",
            "note": "Use supervised labels, graph features, device intelligence, and policy checks in production.",
        }
