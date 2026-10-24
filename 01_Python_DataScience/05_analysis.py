import pandas as pd


df = pd.read_csv("dirty_sales.csv")

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df = df.drop_duplicates()

df = df.dropna(
    subset=["quantity", "price"]
)

df = df[df["quantity"] > 0]

df["revenue"] = (
    df["quantity"] *
    df["price"]
)

south_sales = df[
    df["region"] == "South"
]

print(south_sales)

print("\n===== TOTAL REVENUE FOR SOUTH REGION =====")
print(south_sales["revenue"].sum())

result = df[
    (df["region"] == "South")
    &
    (df["revenue"] > 200000)
]

print(result)

print("\n===== TOTAL REVENUE FOR SOUTH REGION WITH REVENUE > 200000 =====")
print(result["revenue"].sum())

sorted_df = df.sort_values(
    by="revenue",
    ascending=False
)

print(sorted_df)

print("\n===== TOP 5 REVENUE RECORDS =====")
print(sorted_df.head(5))

product_summary = (
    df.groupby("product")
      .agg(
          total_revenue=("revenue", "sum"),
          average_price=("price", "mean"),
          total_quantity=("quantity", "sum")
      )
)

print(product_summary)

print("\n===== TOP 5 PRODUCTS BY TOTAL REVENUE =====")
print(product_summary.sort_values(by="total_revenue", ascending=False).head(5))


region_summary = (
    df.groupby("region")["revenue"]
      .sum()
      .sort_values(
          ascending=False
      )
)

print(region_summary)

print("\n===== TOP REGION BY REVENUE =====")
print(region_summary.head(1))

pivot = pd.pivot_table(
    df,
    values="revenue",
    index="product",
    columns="region",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

print("\n===== TOP 5 PRODUCTS BY REVENUE IN SOUTH REGION =====")
print(pivot.sort_values(by="South", ascending=False).head(5))