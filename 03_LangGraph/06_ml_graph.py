from pathlib import Path
from typing import TypedDict

import pandas as pd

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_absolute_error, r2_score

from langgraph.graph import StateGraph, START, END


DATA_FILE = (
    Path(__file__).resolve().parent
    / ".."
    / "01_Python_DataScience"
    / "sales_100k_raw.csv"
).resolve()


class MLState(TypedDict, total=False):
    quantity: float
    unit_price: float
    discount_pct: float
    marketing_spend: float

    prediction: float

    mae: float
    r2: float

    answer: str


def train_and_predict(state: MLState):
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    numeric_columns = ["quantity", "unit_price", "discount_pct", "marketing_spend"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=numeric_columns)

    df = df[df["quantity"] > 0]

    df = df[df["unit_price"] > 0]

    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"])

    features = ["quantity", "unit_price", "discount_pct", "marketing_spend"]

    X = df[features]

    y = df["net_revenue"]

    (X_train, X_test, y_train, y_test) = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, test_predictions)

    r2 = r2_score(y_test, test_predictions)

    new_order = pd.DataFrame(
        [
            {
                "quantity": state["quantity"],
                "unit_price": state["unit_price"],
                "discount_pct": state["discount_pct"],
                "marketing_spend": state["marketing_spend"],
            }
        ]
    )

    predicted_revenue = float(model.predict(new_order)[0])

    answer = (
        f"Predicted net revenue: "
        f"{predicted_revenue:,.2f}\n"
        f"MAE: {mae:,.2f}\n"
        f"R2: {r2:.4f}"
    )

    return {
        "prediction": predicted_revenue,
        "mae": float(mae),
        "r2": float(r2),
        "answer": answer,
    }


builder = StateGraph(MLState)


builder.add_node("train_and_predict", train_and_predict)


builder.add_edge(START, "train_and_predict")


builder.add_edge("train_and_predict", END)


graph = builder.compile()


result = graph.invoke(
    {"quantity": 3, "unit_price": 65000, "discount_pct": 0.10, "marketing_spend": 700}
)


print(result["answer"])
