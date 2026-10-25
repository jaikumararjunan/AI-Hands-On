from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MarketingDecision:
    segment: str
    next_best_action: str
    rationale: list[str]
    guardrails: list[str]


class MarketingService:
    """Learning-oriented RFM/propensity style decision service.

    Production systems would replace these rules with trained propensity/uplift models,
    experimentation, consent/eligibility checks, frequency caps, and feature-store inputs.
    """

    def decide(self, customer: dict[str, Any]) -> dict[str, Any]:
        days = int(customer.get("days_since_last_order", 999))
        orders = int(customer.get("orders_90d", 0))
        spend = float(customer.get("spend_90d", 0.0))
        churn = float(customer.get("churn_probability", 0.0))
        consent = bool(customer.get("marketing_consent", False))

        if days <= 14 and orders >= 5 and spend >= 50000:
            segment = "VIP_ACTIVE"
            action = "Offer early-access / loyalty benefit, not a blanket discount"
            reasons = ["recent purchase", "high frequency", "high value"]
        elif churn >= 0.70 or days > 60:
            segment = "AT_RISK"
            action = "Retention journey: service check + targeted incentive after eligibility check"
            reasons = ["high churn risk or long inactivity"]
        elif orders == 0:
            segment = "NEW_OR_PROSPECT"
            action = "Onboarding education + socially proven products"
            reasons = ["no recent purchases"]
        else:
            segment = "GROWTH"
            action = "Cross-sell complementary products using recommendation candidates"
            reasons = ["active but not yet VIP"]

        guardrails = [
            "respect marketing consent and channel preferences",
            "apply frequency caps and suppression rules",
            "A/B or uplift-test material changes",
            "do not expose protected/sensitive attributes to the generative prompt",
        ]
        if not consent:
            action = "No outbound marketing; allow only permitted transactional/service communication"
            reasons.append("marketing consent absent")

        return MarketingDecision(segment, action, reasons, guardrails).__dict__

    def campaign_suggestions(self, objective: str) -> dict[str, Any]:
        return {
            "objective": objective,
            "candidate_ideas": [
                "personalized complementary-product recommendation",
                "win-back journey for genuinely at-risk customers",
                "post-purchase education before asking for a review",
                "inventory-aware promotion that avoids unavailable products",
            ],
            "measurement": ["incremental conversion", "margin", "unsubscribe rate", "return rate"],
            "note": "Use an approved LLM only for copy/ideation; eligibility, audience and spend controls stay deterministic.",
        }
