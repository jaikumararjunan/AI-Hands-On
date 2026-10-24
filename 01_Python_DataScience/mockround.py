import pandas as pd

df = pd.read_csv("sales_100k_raw.csv")

#print(df.head())
#print(df.shape)
#print(df.columns.tolist())
#print(df.dtypes)

#print(df.isnull().sum())
#print(df.duplicated().sum())

df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

print(df.dtypes)

df["gross_revenue"] = df["quantity"] * df["unit_price"]

df["discount_amount"] = df["gross_revenue"] * df["discount_pct"]

df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

summary = (
    df.groupby("product")
    .agg(
        total_revenue=("net_revenue", "sum"),
        avg_revenue=("net_revenue", "mean"),
        total_quantity=("quantity", "sum"),
        order_count=("order_id", "count"),
    )
    .sort_values("total_revenue", ascending=False)
)