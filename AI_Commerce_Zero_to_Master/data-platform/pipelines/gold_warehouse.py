from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SILVER_FILE = ROOT / "lake" / "silver" / "orders" / "orders.csv"
WAREHOUSE = ROOT / "warehouse" / "commerce_dw.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS fact_orders (
  event_id TEXT PRIMARY KEY,
  occurred_at TEXT NOT NULL,
  order_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  discount REAL NOT NULL,
  net_revenue REAL NOT NULL,
  region TEXT,
  channel TEXT
);
CREATE TABLE IF NOT EXISTS mart_daily_sales AS SELECT '' AS order_date, 0 AS orders, 0.0 AS revenue WHERE 0;
CREATE TABLE IF NOT EXISTS mart_customer_rfm AS SELECT '' AS customer_id, 0 AS frequency, 0.0 AS monetary WHERE 0;
"""


def run() -> Path:
    WAREHOUSE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(WAREHOUSE)
    try:
        conn.executescript(SCHEMA)
        with SILVER_FILE.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                conn.execute(
                    """INSERT OR REPLACE INTO fact_orders
                    (event_id, occurred_at, order_id, customer_id, product_id, quantity,
                     unit_price, discount, net_revenue, region, channel)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row["event_id"], row["occurred_at"], row["order_id"], row["customer_id"],
                     row["product_id"], int(row["quantity"]), float(row["unit_price"]),
                     float(row["discount"]), float(row["net_revenue"]), row["region"], row["channel"]),
                )
        conn.execute("DELETE FROM mart_daily_sales")
        conn.execute("""INSERT INTO mart_daily_sales
                     SELECT substr(occurred_at,1,10), COUNT(DISTINCT order_id), ROUND(SUM(net_revenue),2)
                     FROM fact_orders GROUP BY substr(occurred_at,1,10)""")
        conn.execute("DELETE FROM mart_customer_rfm")
        conn.execute("""INSERT INTO mart_customer_rfm
                     SELECT customer_id, COUNT(DISTINCT order_id), ROUND(SUM(net_revenue),2)
                     FROM fact_orders GROUP BY customer_id""")
        conn.commit()
    finally:
        conn.close()
    return WAREHOUSE


if __name__ == "__main__":
    print("WAREHOUSE:", run())
