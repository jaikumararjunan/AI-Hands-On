from __future__ import annotations

import argparse
import csv
import json
import random
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def request_json(method: str, url: str, body: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> Any:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else None


def read_customers(dataset: Path) -> list[dict[str, str]]:
    with (dataset / "identity/customers.csv").open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Use generated customer IDs to exercise the running Java and Python learning services.")
    parser.add_argument("--dataset", default="output/latest")
    parser.add_argument("--java-url", default="http://127.0.0.1:8080")
    parser.add_argument("--python-url", default="http://127.0.0.1:8000")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    dataset = Path(args.dataset)
    if not dataset.is_absolute():
        dataset = root / dataset
    rng = random.Random(args.seed)
    customers = read_customers(dataset)

    try:
        products = request_json("GET", f"{args.java_url}/api/products")
    except Exception as error:
        raise SystemExit(f"Java service unavailable at {args.java_url}: {error}")

    print(f"Java products available: {len(products)}")
    print(f"Generated customers available: {len(customers)}")

    for i in range(args.count):
        customer = rng.choice(customers)
        product = rng.choice(products)
        quantity = rng.randint(1, 2)
        cid = customer["customer_id"]
        pid = product["id"]

        print("\n" + "=" * 72)
        print(f"FLOW {i+1}: customer={cid} product={pid} quantity={quantity}")

        cart = request_json(
            "POST",
            f"{args.java_url}/api/carts/{urllib.parse.quote(cid)}/items",
            {"productId": pid, "quantity": quantity},
        )
        print("Cart:", json.dumps(cart, indent=2))

        checkout = request_json(
            "POST",
            f"{args.java_url}/api/checkout",
            {
                "order": {
                    "customerId": cid,
                    "items": [{"productId": pid, "quantity": quantity}],
                    "couponCode": "LEARN10" if i == 0 else None,
                },
                "currency": "INR",
                "paymentMethodRef": f"pm_learning_{i+1}",
            },
            {"Idempotency-Key": f"mock-seed-{cid}-{i+1}"},
        )
        print("Checkout:", json.dumps(checkout, indent=2))

        try:
            q = urllib.parse.quote(product["name"])
            ai_search = request_json("GET", f"{args.python_url}/ai/search?q={q}&limit=3")
            print("AI search:", json.dumps(ai_search, indent=2))
            recs = request_json("GET", f"{args.python_url}/ai/recommendations/{urllib.parse.quote(cid)}?limit=3")
            print("Recommendations:", json.dumps(recs, indent=2))
        except Exception as error:
            print(f"Python AI service not available; Java flow still succeeded. Detail: {error}")


if __name__ == "__main__":
    main()
