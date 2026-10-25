from __future__ import annotations

import argparse
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

SERVICES = [
    "catalog-service", "search-service", "cart-service", "checkout-service",
    "payment-service", "order-service", "inventory-service", "shipping-service",
    "returns-service", "marketing-service", "ai-service", "mcp-service"
]
EVENTS = {
    "catalog-service": ["product.viewed", "product.updated"],
    "search-service": ["search.executed", "search.clicked"],
    "cart-service": ["cart.item_added", "cart.item_removed"],
    "checkout-service": ["checkout.started", "checkout.completed"],
    "payment-service": ["payment.succeeded", "payment.failed"],
    "order-service": ["order.created", "order.cancelled"],
    "inventory-service": ["inventory.reserved", "inventory.low_stock"],
    "shipping-service": ["shipment.created", "shipment.delivered"],
    "returns-service": ["return.requested", "return.refunded"],
    "marketing-service": ["campaign.sent", "campaign.clicked"],
    "ai-service": ["recommendation.generated", "fraud.scored", "forecast.generated"],
    "mcp-service": ["mcp.tool_called", "mcp.tool_completed"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit synthetic cross-service events continuously for observability and streaming labs.")
    parser.add_argument("--output", default="output/live/events.jsonl")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--count", type=int, default=0, help="0 means continue until Ctrl+C")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    emitted = 0
    print(f"Streaming to {out}. Press Ctrl+C to stop.")
    try:
        while args.count == 0 or emitted < args.count:
            service = rng.choice(SERVICES)
            event = {
                "event_id": f"LIVE-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
                "service": service,
                "event_type": rng.choice(EVENTS[service]),
                "occurred_at": datetime.now(timezone.utc).isoformat(),
                "trace_id": f"{rng.getrandbits(128):032x}",
                "payload": {
                    "customer_id": f"CUST-{rng.randint(1, 500):06d}",
                    "product_id": f"P-{rng.randint(1, 300):06d}",
                    "latency_ms": rng.randint(5, 1200),
                },
            }
            with out.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event) + "\n")
            print(json.dumps(event))
            emitted += 1
            time.sleep(max(0.01, args.interval))
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
