from pathlib import Path
from langchain.tools import tool

import pandas as pd


DATA_FILE = (
    Path(__file__).resolve().parent
    / ".."
    / "01_Python_DataScience"
    / "sales_100k_raw.csv"
).resolve()

print("Dataset:", DATA_FILE)
print("Exists:", DATA_FILE.exists())

def load_clean_sales():

    df = pd.read_csv(DATA_FILE)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df = df.drop_duplicates()

    df = df.dropna(subset=["quantity", "unit_price", "region"])

    df = df[df["quantity"] > 0]

    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    df["discount_amount"] = df["gross_revenue"] * df["discount_pct"]

    df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

    return df


@tool
def get_total_revenue() -> str:
    """
    Calculate the total net revenue
    from the sales dataset.
    """

    df = load_clean_sales()

    total = df["net_revenue"].sum()

    return f"{total:,.2f}"


@tool
def get_top_products(limit: int = 5) -> str:
    """
    Return products ranked by total net revenue.

    Use this when asked about top,
    best, or highest-revenue products.
    """

    df = load_clean_sales()

    result = (
        df.groupby("product")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )

    return result.to_string()


@tool
def get_region_revenue() -> str:
    """
    Calculate total net revenue by region.
    """

    df = load_clean_sales()

    result = df.groupby("region")["net_revenue"].sum().sort_values(ascending=False)

    return result.to_string()


print(get_total_revenue.invoke({}))


print(get_top_products.invoke({"limit": 3}))


print(get_region_revenue.invoke({}))
