import pandas as pd


df = pd.read_csv("sales.csv")


print("===== RAW DATA =====")
print(df)


print("\n===== DATA INFORMATION =====")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


df["revenue"] = (
    df["quantity"] *
    df["price"]
)


print("\n===== DATA WITH REVENUE =====")
print(df)


total_revenue = df["revenue"].sum()

print("\n===== TOTAL REVENUE =====")
print(total_revenue)


revenue_by_product = (
    df.groupby("product")["revenue"]
      .sum()
      .sort_values(ascending=False)
)


print("\n===== REVENUE BY PRODUCT =====")
print(revenue_by_product)