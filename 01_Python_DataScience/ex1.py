import os

print(os.getcwd())
print(os.listdir())


import pandas as pd


df = pd.read_csv("sales.csv")


df["revenue"] = (
    df["quantity"] *
    df["price"]
)


product_result = (
    df.groupby("product")["revenue"]
      .sum()
      .sort_values(
          ascending=False
      )
)


region_result = (
    df.groupby("region")["revenue"]
      .sum()
      .sort_values(
          ascending=False
      )
)


print(
    "Revenue by Product"
)

print(
    product_result
)


print(
    "\nRevenue by Region"
)

print(
    region_result
)