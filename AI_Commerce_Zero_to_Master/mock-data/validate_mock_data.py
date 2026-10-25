from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check(name: str, condition: bool, detail: str = "") -> tuple[str, bool, str]:
    return name, condition, detail


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate referential integrity of generated AI Commerce mock data.")
    parser.add_argument("dataset", nargs="?", default="output/latest")
    args = parser.parse_args()
    root = Path(args.dataset)
    if not root.is_absolute():
        root = Path(__file__).resolve().parent / root

    customers = read_csv(root / "identity/customers.csv")
    products = read_csv(root / "catalog/products.csv")
    orders = read_csv(root / "orders/orders.csv")
    order_items = read_csv(root / "orders/order_items.csv")
    payments = read_csv(root / "payments/payment_intents.csv")
    shipments = read_csv(root / "shipping/shipments.csv")
    returns = read_csv(root / "returns/returns.csv")
    inventory = read_csv(root / "inventory/inventory.csv")
    warehouses = read_csv(root / "inventory/warehouses.csv")

    customer_ids = {x["customer_id"] for x in customers}
    product_ids = {x["product_id"] for x in products}
    order_ids = {x["order_id"] for x in orders}
    warehouse_ids = {x["warehouse_id"] for x in warehouses}

    results = [
        check("manifest exists", (root / "manifest.json").exists()),
        check("orders -> customers", all(x["customer_id"] in customer_ids for x in orders)),
        check("order_items -> orders", all(x["order_id"] in order_ids for x in order_items)),
        check("order_items -> products", all(x["product_id"] in product_ids for x in order_items)),
        check("payments -> orders", all(x["order_id"] in order_ids for x in payments)),
        check("shipments -> orders", all(x["order_id"] in order_ids for x in shipments)),
        check("returns -> orders", all(x["order_id"] in order_ids for x in returns)),
        check("inventory -> products", all(x["product_id"] in product_ids for x in inventory)),
        check("inventory -> warehouses", all(x["warehouse_id"] in warehouse_ids for x in inventory)),
        check("payment idempotency unique", len({x["idempotency_key"] for x in payments}) == len(payments)),
    ]

    jsonl_paths = [
        root / "events/service_events.jsonl",
        root / "data-platform/order_events.jsonl",
        root / "ai/vector_corpus.jsonl",
        root / "observability/service_logs.jsonl",
    ]
    for path in jsonl_paths:
        valid = True
        if not path.exists():
            valid = False
        else:
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        json.loads(line)
            except Exception:
                valid = False
        results.append(check(f"valid jsonl: {path.relative_to(root)}", valid))

    print("MOCK DATA VALIDATION")
    print("=" * 72)
    failed = 0
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL':4s}  {name} {detail}")
        if not ok:
            failed += 1
    print("=" * 72)
    if failed:
        raise SystemExit(f"Validation failed: {failed} check(s)")
    print("All referential-integrity and file-format checks passed.")


if __name__ == "__main__":
    main()
