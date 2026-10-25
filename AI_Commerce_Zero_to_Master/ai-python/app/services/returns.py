import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class ReturnRiskService:
    def __init__(self):
        rng = np.random.default_rng(11)
        n = 3000
        df = pd.DataFrame({
            "price": rng.lognormal(mean=9.0, sigma=0.8, size=n),
            "discount_pct": rng.uniform(0, 0.5, n),
            "prior_return_rate": rng.uniform(0, 0.8, n),
            "delivery_delay_days": rng.poisson(1.2, n),
            "rating": rng.uniform(1, 5, n),
        })
        logits = (
            1.6 * df["prior_return_rate"]
            + 1.0 * df["discount_pct"]
            + 0.12 * df["delivery_delay_days"]
            - 0.45 * (df["rating"] - 3)
            - 1.4
        )
        probs = 1 / (1 + np.exp(-logits))
        y = (rng.random(n) < probs).astype(int)
        self.columns = list(df.columns)
        self.model = LogisticRegression(max_iter=500).fit(df, y)

    def score(self, payload: dict):
        row = pd.DataFrame([{c: payload[c] for c in self.columns}])
        probability = float(self.model.predict_proba(row)[0, 1])
        return {
            "return_probability": round(probability, 4),
            "risk_band": "HIGH" if probability >= 0.65 else ("MEDIUM" if probability >= 0.35 else "LOW"),
            "recommended_action": "Improve product/size/delivery information; do not block legitimate purchases solely on this score.",
        }
