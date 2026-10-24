from typing import TypedDict
from pathlib import Path

import pandas as pd


DATA_FILE = (
    Path(__file__).resolve().parent
    / ".."
    / "01_Python_DataScience"
    / "sales_100k_raw.csv"
).resolve()


class SalesState(TypedDict, total=False):
    question: str

    route: str

    answer: str


def analyze_sales(state: SalesState):

    df = pd.read_csv(DATA_FILE)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df = df.drop_duplicates()

    df = df.dropna(subset=["quantity", "unit_price"])

    df = df[df["quantity"] > 0]

    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"])

    result = (
        df.groupby("product")["net_revenue"].sum().sort_values(ascending=False).head(3)
    )

    return {"answer": result.to_string()}
