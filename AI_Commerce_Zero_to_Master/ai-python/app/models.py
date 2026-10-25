from pydantic import BaseModel, Field
from typing import List

class SearchResult(BaseModel):
    product_id: str
    name: str
    score: float

class FraudRequest(BaseModel):
    amount: float
    quantity: int
    discount_pct: float = 0.0
    account_age_days: int = 365
    orders_last_hour: int = 1

class ForecastRequest(BaseModel):
    daily_sales: List[float] = Field(min_length=7)
    horizon_days: int = Field(default=7, ge=1, le=90)

class AgentRequest(BaseModel):
    question: str


class PricingRequest(BaseModel):
    base_price: float
    inventory_units: int
    demand_index: float = 1.0
    competitor_price: float | None = None
    min_price: float
    max_price: float

class ChurnRequest(BaseModel):
    days_since_last_order: int
    orders_90d: int
    returns_90d: int
    support_tickets_90d: int
    email_engagement: float

class ReturnRiskRequest(BaseModel):
    price: float
    discount_pct: float
    prior_return_rate: float
    delivery_delay_days: int
    rating: float

class ReviewRequest(BaseModel):
    text: str


class MarketingDecisionRequest(BaseModel):
    days_since_last_order: int = 999
    orders_90d: int = 0
    spend_90d: float = 0.0
    churn_probability: float = Field(default=0.0, ge=0.0, le=1.0)
    marketing_consent: bool = False

class CampaignSuggestionRequest(BaseModel):
    objective: str
