import pandas as pd

from sklearn.linear_model import LinearRegression


data = {
    "advertising": [
        10,
        20,
        30,
        40,
        50
    ],

    "sales": [
        100,
        180,
        260,
        350,
        430
    ]
}


df = pd.DataFrame(data)


X = df[["advertising"]]

y = df["sales"]


model = LinearRegression()


model.fit(X, y)  # type: ignore


prediction = model.predict(pd.DataFrame({"advertising": [60]}))


print(
    "Predicted sales:",
    prediction[0]
)
