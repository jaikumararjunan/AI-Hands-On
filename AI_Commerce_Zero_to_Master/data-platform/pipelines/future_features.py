from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse" / "commerce_dw.db"
FEATURE_FILE = ROOT / "features" / "customer_features.csv"


def run() -> Path:
    conn = sqlite3.connect(WAREHOUSE)
    try:
        rows = conn.execute(
            """SELECT customer_id,
                      COUNT(DISTINCT order_id) AS lifetime_orders,
                      ROUND(SUM(net_revenue),2) AS lifetime_revenue,
                      ROUND(AVG(net_revenue),2) AS avg_order_value,
                      MAX(substr(occurred_at,1,10)) AS last_order_date
               FROM fact_orders GROUP BY customer_id"""
        ).fetchall()
    finally:
        conn.close()
    FEATURE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with FEATURE_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["customer_id", "lifetime_orders", "lifetime_revenue", "avg_order_value", "last_order_date"])
        writer.writerows(rows)
    return FEATURE_FILE


if __name__ == "__main__":
    print("FEATURES:", run())
