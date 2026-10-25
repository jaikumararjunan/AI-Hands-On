# Mock Data Relationships and Service Ownership

## Core identity chain

```text
customers.customer_id
  -> addresses.customer_id
  -> devices.customer_id
  -> loyalty_accounts.customer_id
  -> carts.customer_id
  -> orders.customer_id
  -> reviews.customer_id
  -> support_tickets.customer_id
  -> marketing_events.customer_id
```

## Commerce lifecycle

```text
carts.cart_id
  -> cart_items.cart_id
  -> orders.cart_id

orders.order_id
  -> order_items.order_id
  -> payment_intents.order_id
  -> shipments.order_id
  -> returns.order_id
  -> support_tickets.order_id
```

## Product / marketplace

```text
categories.category_id
  <- products.category_id

sellers.seller_id
  <- products.seller_id
  <- order_items.seller_id

products.product_id
  <- prices.product_id
  <- inventory.product_id
  <- cart_items.product_id
  <- order_items.product_id
  <- reviews.product_id
  <- search_events.clicked_product_id
```

## Payments

```text
orders.order_id
  -> payment_intents.order_id
  -> payment_transactions.order_id

payment_intents.payment_id
  -> payment_transactions.payment_id
  -> payment_webhooks.payment_id
  -> refunds.payment_id
```

`payment_method_ref` is synthetic and provider-style. The generator never creates a card PAN, CVV, bank password, or real financial credential.

## Inventory / fulfilment

```text
warehouses.warehouse_id
  -> inventory.warehouse_id
  -> reservations.warehouse_id

orders.order_id
  -> reservations.order_id
  -> shipments.order_id

shipments.shipment_id
  -> tracking_events.shipment_id
```

## ML and DL learning views

| Dataset | Learning task |
|---|---|
| `ml/fraud_training.csv` | classification / anomaly detection |
| `ml/churn_training.csv` | churn classification / retention |
| `ml/return_risk_training.csv` | return propensity |
| `ml/recommendation_interactions.csv` | collaborative filtering / two-tower preparation |
| `ml/demand_daily.csv` | time-series forecasting / LSTM/TFT preparation |
| `ml/review_sentiment.csv` | NLP / sentiment |
| `ml/search_ranking.csv` | learning-to-rank / semantic ranking |

## GenAI / RAG / Agentic views

| File | Use |
|---|---|
| `ai/rag_documents.jsonl` | document ingestion |
| `ai/vector_corpus.jsonl` | chunk + embedding + vector DB |
| `ai/agent_test_cases.jsonl` | agent evaluation |
| `ai/agent_traces.jsonl` | trajectory/tool-call analysis |

## Platform / SRE views

| File | Use |
|---|---|
| `events/service_events.jsonl` | Kafka/event-driven labs |
| `observability/service_logs.jsonl` | log analysis |
| `observability/service_traces.csv` | distributed tracing |
| `observability/service_metrics.csv` | dashboards/SLO exercises |
| `data-platform/order_events.jsonl` | Bronze -> Silver -> Warehouse pipeline |
