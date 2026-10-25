from collections import Counter
from app.catalog import PRODUCTS, CUSTOMER_HISTORY

class RecommendationService:
    def recommend(self, customer_id: str, limit: int = 4):
        history = CUSTOMER_HISTORY.get(customer_id, [])
        affinity = Counter(history)
        scored = []
        for product in PRODUCTS:
            score = affinity.get(product["category"], 0) * 2.0
            # Simple legacy-style priors: accessories and monitors cross-sell well with laptops.
            if "laptop" in history and product["category"] in {"monitor", "accessory"}:
                score += 1.0
            scored.append((score, product))
        scored.sort(key=lambda x: (x[0], -x[1]["price"]), reverse=True)
        return [
            {"product_id": p["id"], "name": p["name"], "score": score, "reason": "category affinity + cross-sell rule"}
            for score, p in scored[:limit]
        ]
