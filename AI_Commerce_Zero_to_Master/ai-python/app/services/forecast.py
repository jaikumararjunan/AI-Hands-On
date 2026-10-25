import numpy as np
from sklearn.linear_model import LinearRegression

class ForecastService:
    def forecast(self, daily_sales: list[float], horizon_days: int):
        y = np.asarray(daily_sales, dtype=float)
        x = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        future_x = np.arange(len(y), len(y) + horizon_days).reshape(-1, 1)
        predictions = model.predict(future_x)
        return {
            "forecast": [round(max(0.0, float(v)), 2) for v in predictions],
            "method": "linear trend baseline",
            "upgrade_path": "gradient boosting -> temporal deep learning/TFT for richer seasonal signals",
        }
