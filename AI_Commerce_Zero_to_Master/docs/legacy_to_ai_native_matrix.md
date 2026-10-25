# Legacy -> Modern -> AI-Native E-commerce Matrix

| Domain | Legacy | Modern ML/DL | AI-native / Agentic | Project code |
|---|---|---|---|---|
| Search | SQL LIKE / keyword | Learning-to-rank, embeddings | Conversational + multimodal + agent-assisted search | `ai-python/app/services/search.py` |
| Recommendations | Best sellers / rules | Collaborative filtering, two-tower | Conversational intent + long-term memory + multimodal taste | `recommendation.py`, `dl/two_tower.py` |
| Promotions | Static coupons | Propensity/uplift models | Policy-controlled agent proposes campaign, human approves | Java `PromotionService` + agent roadmap |
| Fraud | Threshold rules | Gradient boosting, anomaly models, graph features | Risk agent explains evidence; policy engine owns blocking | `fraud.py`, `dl/fraud_autoencoder.py` |
| Forecasting | Moving average | GBM/LSTM/TFT | Forecast agent combines model + events + inventory tools | `forecast.py`, `dl/demand_lstm.py` |
| Support | FAQ / call center | Intent classification | RAG + tool-using service agent + human handoff | `rag.py`, `agent.py` |
| Merchandising | Manual category pages | Ranking/optimization | Merchant copilot proposes changes and simulations | roadmap/docs |
| Checkout | Form + payment | Fraud/ETA | Agentic cart/checkout with explicit permissions | contracts/agent-commerce |
| Observability | Logs | Metrics/APM | Agent traces, quality evals, prompt/model cost and safety | infra + observability docs |
