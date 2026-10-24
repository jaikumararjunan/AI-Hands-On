import pandas as pd

df = pd.read_csv("dirty_sales.csv")
print("Original DataFrame:")
print(df)

print("===== ORIGINAL DATA =====")
print(df)


print("\n===== SHAPE =====")
print(df.shape)


print("\n===== DATA TYPES =====")
print(df.dtypes)


print("\n===== NULL VALUES =====")
print(df.isnull().sum())


print("\n===== DUPLICATES =====")
print(df.duplicated().sum())

print("\n===== CLEANING DATA =====")

# Drop duplicates
df = df.drop_duplicates()

# Fill missing values for 'quantity' with 0
df['quantity'] = df['quantity'].fillna(0)

# Fill missing values for 'price' with 0
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

print("Cleaned DataFrame:")
print(df)

print("\n===== CLEANED SHAPE =====")
print(df.shape)

print("\n===== CLEANED NULL VALUES =====")
print(df.isnull().sum())

print("\n===== CLEANED DUPLICATES =====")
print(df.duplicated().sum())

print("\n===== FINAL CLEANED DATA =====")
print(df)

# Save the cleaned DataFrame to a new CSV file
df.to_csv("cleaned_sales.csv", index=False)

print("\nCleaned data saved to 'cleaned_sales.csv'")

df["price"] = pd.to_numeric(    df["price"] , 
                                    errors='coerce'
                            )
print("DataFrame after converting 'price' to numeric:")
print(df.dtypes)
print("DataFrame after dropping duplicates:")
print(df.isnull().sum())

df = df.drop_duplicates()
print("\n===== DUPLICATES AFTER DROPPING =====")
print(df.duplicated().sum())

print("\n===== FINAL DATA TYPES =====")
print(df.dtypes)


print("\n ================== +++++++")
df = df.dropna(
    subset=["quantity", "price"]
)
print("\n===== DATA AFTER DROPPING NA =====")
print(df)
print("\n===== FINAL SHAPE =====")
print(df.shape)

print("\n ==========Invalid Quantites ========")
df = df[ df["quantity"] > 0 ]
print("\n===== DATA AFTER REMOVING INVALID QUANTITIES =====")
print(df)

df["revenue"] = (
    df["quantity"] *
    df["price"]
)
print("\n===== DATA WITH REVENUE =====")
print(df)