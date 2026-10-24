from pathlib import Path
from typing import TypedDict

import pandas as pd

from langgraph.graph import StateGraph, START, END


DATA_FILE = (
    Path(__file__).resolve().parent
    / ".."
    / "01_Python_DataScience"
    / "sales_100k_raw.csv"
).resolve()


class SalesState(TypedDict, total=False):
    question: str
    answer: str
    rows_before: int
    rows_after: int


def analyze_sales(state: SalesState):
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    rows_before = len(df)

    # Convert bad numeric values.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Remove exact duplicate records.
    df = df.drop_duplicates()

    # Remove rows unusable for revenue analysis.
    df = df.dropna(subset=["quantity", "unit_price", "region"])

    # Business validation.
    df = df[df["quantity"] > 0]

    df = df[df["unit_price"] > 0]

    # Feature engineering.
    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    df["discount_amount"] = df["gross_revenue"] * df["discount_pct"]

    df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

    rows_after = len(df)

    # Business analysis.
    result = (
        df.groupby("product")["net_revenue"].sum().sort_values(ascending=False).head(3)
    )

    answer = "Top 3 products by net revenue:\n\n" + result.to_string()

    return {"answer": answer, "rows_before": rows_before, "rows_after": rows_after}


builder = StateGraph(SalesState)


builder.add_node("analyze_sales", analyze_sales)


builder.add_edge(START, "analyze_sales")


builder.add_edge("analyze_sales", END)


graph = builder.compile()


result = graph.invoke({"question": "Which 3 products generate the highest revenue?"})


print("Dataset:", DATA_FILE)

print("Rows before cleaning:", result["rows_before"])

print("Rows after cleaning:", result["rows_after"])

print()

print(result["answer"])
