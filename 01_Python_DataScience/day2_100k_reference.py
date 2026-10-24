"""
DAY 2 - 100K ROW HANDS-ON REFERENCE
Type these sections yourself during practice. Use this file only as a backup/reference.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

FILE = "sales_100k_raw.csv"

# 1) NumPy basics
numbers = np.array([10, 20, 30, 40, 50])
print("NumPy mean:", numbers.mean())
print("Vectorized x 2:", numbers * 2)

# 2) Read CSV
df = pd.read_csv(FILE)
print(df.head())
print("Shape:", df.shape)

# 3) Inspect
print(df.info())
print(df.dtypes)
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

# 4) Convert datatypes
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["marketing_spend"] = pd.to_numeric(df["marketing_spend"], errors="coerce")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# 5) Remove duplicates
df = df.drop_duplicates()

# 6) Handle invalid / missing values
df = df.dropna(subset=["quantity", "unit_price", "region", "order_date"])
df = df[df["quantity"] > 0]
df = df[df["unit_price"] > 0]

# Optional business rule: exclude unrealistic future dates
today = pd.Timestamp.today().normalize()
df = df[df["order_date"] <= today]

# 7) Calculate columns
df["gross_revenue"] = df["quantity"] * df["unit_price"]
df["discount_amount"] = df["gross_revenue"] * df["discount_pct"]
df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

# 8) Filter
south_high_value = df[
    (df["region"] == "South") &
    (df["net_revenue"] > 100000)
]
print("South high-value orders:", south_high_value.shape)

# 9) Sort
top_orders = df.sort_values("net_revenue", ascending=False).head(10)
print(top_orders[["order_id","product","region","net_revenue"]])

# 10) GroupBy + aggregations
product_summary = (
    df.groupby("product")
      .agg(
          total_revenue=("net_revenue", "sum"),
          avg_order_value=("net_revenue", "mean"),
          total_quantity=("quantity", "sum"),
          order_count=("order_id", "count")
      )
      .sort_values("total_revenue", ascending=False)
)
print(product_summary)

# 11) Pivot table
pivot = pd.pivot_table(
    df,
    values="net_revenue",
    index="category",
    columns="region",
    aggfunc="sum",
    fill_value=0
)
print(pivot)

# 12) Visualization
product_summary["total_revenue"].head(10).plot(
    kind="bar",
    title="Top Products by Net Revenue"
)
plt.xlabel("Product")
plt.ylabel("Net Revenue")
plt.tight_layout()
plt.savefig("top_products_revenue.png")
plt.close()

# 13) ML: feature vs target
# Predict net_revenue from selected numerical features.
features = ["quantity", "unit_price", "discount_pct", "marketing_spend"]
target = "net_revenue"

ml_df = df[features + [target]].dropna()

X = ml_df[features]
y = ml_df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, predictions))
print("R2:", r2_score(y_test, predictions))

new_order = pd.DataFrame([{
    "quantity": 3,
    "unit_price": 65000,
    "discount_pct": 0.10,
    "marketing_spend": 700
}])

print("Predicted revenue:", model.predict(new_order)[0])

# 14) Useful debug commands
print(df.columns.tolist())
print(df.dtypes)
print(df.shape)
print(df.head())
print(df.isnull().sum())

# Intentional debugging exercises:
# A) df["qty"] -> KeyError
# B) pd.read_csv("wrong_file.csv") -> FileNotFoundError
# C) compare df["quantity"] > "5" -> datatype issue
