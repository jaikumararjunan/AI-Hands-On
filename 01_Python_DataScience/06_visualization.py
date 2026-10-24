import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("sales.csv")

df["revenue"] = (
    df["quantity"] *
    df["price"]
)


product_revenue = (
    df.groupby("product")["revenue"]
      .sum()
)


product_revenue.plot(
    kind="bar",
    title="Revenue by Product"
)


plt.xlabel("Product")
plt.ylabel("Revenue")

plt.tight_layout()

plt.show()