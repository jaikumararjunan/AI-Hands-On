# AI Commerce Mock Data Generator

This subsystem creates **one synthetic, cross-linked e-commerce world** for every layer of the learning project.

It deliberately generates **no real customers and no real payment-card data**. Payment records use safe provider-style references such as `pm-XXXX`, never PAN/CVV.

## Why one generator?

A common learning mistake is to make a separate random CSV for every microservice. Those files do not agree with each other. This generator preserves the important relationships:

```text
Customer
  -> Address / Device / Loyalty
  -> Cart
  -> Order -> Order Items -> Product / Seller
  -> Payment -> Transaction -> Webhook / Refund
  -> Inventory Reservation -> Warehouse
  -> Shipment -> Tracking
  -> Return -> Refund
  -> Review / Support
  -> Search / Clickstream / Marketing
  -> ML features / RAG / Agent traces / Observability
```

## First run - fresher level

```powershell
cd mock-data
python .\generate_mock_data.py --profile tiny --scenario normal --reset
python .\validate_mock_data.py
```

Start with:

- `output/latest/manifest.json`
- `output/latest/dataset_stats.json`
- `identity/customers.csv`
- `catalog/products.csv`
- `orders/orders.csv`
- `payments/payment_intents.csv`

## Profiles

| Profile | Best for | Customers | Products | Orders |
|---|---|---:|---:|---:|
| tiny | Fresher / file inspection | 25 | 30 | 80 |
| small | 3-year developer labs | 500 | 300 | 2,500 |
| medium | 5-year integration/data labs | 5,000 | 2,000 | 25,000 |
| large | 7-year scale/performance design | 20,000 | 8,000 | 100,000 |
| xlarge | 7+/architect capacity experiments | 50,000 | 15,000 | 250,000 |

Large/xlarge are intentionally heavy but bounded for a laptop learning lab. Real billion-event tests should use partitioned/distributed data producers rather than one Python process.

## Scenarios

```text
normal
peak-sale
fraud-attack
inventory-shortage
payment-degradation
returns-spike
marketing-campaign
mixed-chaos
```

Example:

```powershell
python .\generate_mock_data.py `
  --profile small `
  --scenario payment-degradation `
  --seed 42 `
  --reset
```

The same data model is used, but failure rates, latency, return rates, inventory and traffic change.

## Connect to the existing Bronze -> Silver -> Warehouse lab

Generate and explicitly copy order events into the data-platform sample location:

```powershell
python .\generate_mock_data.py `
  --profile small `
  --scenario normal `
  --reset `
  --sync-data-platform

cd ..\data-platform\pipelines
python .\run_pipeline.py
```

## Real-time stream simulation

```powershell
cd mock-data
python .\stream_mock_events.py --interval 0.5
```

This continuously appends synthetic service events for Kafka/streaming/observability exercises.

## Generated domains

### Transactional
- Identity/customer/address/device/loyalty
- Catalog/category/product/seller
- Pricing/promotions/coupons
- Cart/checkout/order/order items
- Payment intents/transactions/webhooks/refunds
- Inventory/warehouse/reservations
- Fulfilment/shipping/tracking
- Returns/reviews/support
- Marketing/search/clickstream

### ML/DL
- Fraud training
- Churn training
- Return-risk training
- Recommendation interactions
- Daily demand time series
- Review sentiment labels
- Search ranking examples

### GenAI/Agentic
- RAG documents
- Vector chunks
- Agent test cases
- Tool/trajectory traces

### Platform/SRE
- Cross-service domain events
- Synthetic logs
- Traces
- Service-level metrics
- Data-lake-compatible order events

## Learning path

```text
Fresher
  tiny + normal
  learn rows, IDs, CSV, joins

3 years
  small + normal/failure scenario
  APIs, service ownership, debugging

5 years
  medium
  event integration, lake/warehouse, ML features

7 years
  large
  scale, SLOs, queues, back-pressure, hot partitions

7+ / Principal
  large/xlarge + mixed-chaos
  capacity, architecture tradeoffs, DR, governance, cost, failure domains
```

## Reproducibility

`--seed 42` makes the pseudo-random choices repeatable for the same profile, scenario and `--as-of` timestamp. For exact repeatability, specify `--as-of` too:

```powershell
python .\generate_mock_data.py --profile tiny --seed 42 --as-of 2026-10-25T00:00:00+00:00 --reset
```
