import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class ChurnService:
    def __init__(self):
        rng = np.random.default_rng(7)
        n = 3000
        df = pd.DataFrame({
            "days_since_last_order": rng.integers(1, 365, n),
            "orders_90d": rng.poisson(2.0, n),
            "returns_90d": rng.poisson(0.4, n),
            "support_tickets_90d": rng.poisson(0.5, n),
            "email_engagement": rng.uniform(0, 1, n),
        })
        logits = (
            0.012 * df["days_since_last_order"]
            - 0.45 * df["orders_90d"]
            + 0.55 * df["returns_90d"]
            + 0.35 * df["support_tickets_90d"]
            - 1.6 * df["email_engagement"]
            - 1.0
        )
        probs = 1 / (1 + np.exp(-logits))
        y = (rng.random(n) < probs).astype(int)
        self.columns = list(df.columns)
        self.model = LogisticRegression(max_iter=500).fit(df, y)

    def score(self, payload: dict):
        row = pd.DataFrame([{c: payload[c] for c in self.columns}])
        probability = float(self.model.predict_proba(row)[0, 1])
        return {
            "churn_probability": round(probability, 4),
            "segment": "HIGH" if probability >= 0.7 else ("MEDIUM" if probability >= 0.4 else "LOW"),
            "next_step": "Use as a retention signal; do not automatically spam or penalize the customer.",
        }
