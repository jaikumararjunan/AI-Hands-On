from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "lake" / "bronze" / "order_events"
SILVER_FILE = ROOT / "lake" / "silver" / "orders" / "orders.csv"
FIELDS = [
    "event_id", "occurred_at", "order_id", "customer_id", "product_id",
    "quantity", "unit_price", "discount", "net_revenue", "region", "channel"
]


def run() -> Path:
    rows: dict[str, dict] = {}
    for path in BRONZE.rglob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)["payload"]
            quantity = int(payload["quantity"])
            unit_price = float(payload["unit_price"])
            discount = float(payload.get("discount", 0.0))
            if quantity <= 0 or unit_price <= 0:
                continue
            payload["quantity"] = quantity
            payload["unit_price"] = unit_price
            payload["discount"] = discount
            payload["net_revenue"] = round(quantity * unit_price - discount, 2)
            rows[payload["event_id"]] = {field: payload.get(field) for field in FIELDS}
    SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SILVER_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(sorted(rows.values(), key=lambda row: row["occurred_at"]))
    return SILVER_FILE


if __name__ == "__main__":
    print("SILVER:", run())
