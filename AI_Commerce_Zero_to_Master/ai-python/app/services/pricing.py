class PricingService:
    def recommend(self, base_price: float, inventory_units: int, demand_index: float,
                  competitor_price: float | None, min_price: float, max_price: float):
        candidate = base_price
        if demand_index > 1.2 and inventory_units < 20:
            candidate *= 1.04
        elif demand_index < 0.8 or inventory_units > 300:
            candidate *= 0.96
        if competitor_price:
            candidate = 0.7 * candidate + 0.3 * competitor_price
        final_price = min(max(candidate, min_price), max_price)
        return {
            "recommended_price": round(final_price, 2),
            "unconstrained_candidate": round(candidate, 2),
            "guardrails": {"min_price": min_price, "max_price": max_price},
            "note": "Learning demo only. Production pricing needs legal/fairness review, elasticity evidence, margin rules, audit and experiments.",
        }
