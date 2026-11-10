"""
Regression Module - Cost and Time Estimation
Uses Ridge Regression and Random Forest Regressor.
Estimates total trip cost and time based on trip parameters.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "saved_models"


class TripRegressor:
    def __init__(self):
        self.cost_model = None
        self.time_model = None
        self.cost_ridge = None
        self.time_ridge = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.evaluation_results = {}
        self.actual_vs_predicted_cost = []
        self.actual_vs_predicted_time = []

    def train(self, X_train, X_test, y_cost_train, y_cost_test, y_time_train, y_time_test):
        """Train Ridge Regression and Random Forest for cost and time."""
        self.feature_names = list(X_train.columns)

        # Scale features
        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s = self.scaler.transform(X_test)

        # --- Cost Estimation ---
        print("Training cost regressors...")
        self.cost_ridge = Ridge(alpha=10.0)
        self.cost_ridge.fit(X_train_s, y_cost_train)
        cost_ridge_pred = self.cost_ridge.predict(X_test_s)

        rf_cost = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
        rf_cost.fit(X_train, y_cost_train)
        cost_rf_pred = rf_cost.predict(X_test)

        # --- Time Estimation ---
        print("Training time regressors...")
        self.time_ridge = Ridge(alpha=5.0)
        self.time_ridge.fit(X_train_s, y_time_train)
        time_ridge_pred = self.time_ridge.predict(X_test_s)

        rf_time = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1)
        rf_time.fit(X_train, y_time_train)
        time_rf_pred = rf_time.predict(X_test)

        # Choose best models based on R2
        if r2_score(y_cost_test, cost_rf_pred) > r2_score(y_cost_test, cost_ridge_pred):
            self.cost_model = rf_cost
            cost_pred = cost_rf_pred
            best_cost_name = "Random Forest"
        else:
            self.cost_model = self.cost_ridge
            cost_pred = cost_ridge_pred
            best_cost_name = "Ridge Regression"

        if r2_score(y_time_test, time_rf_pred) > r2_score(y_time_test, time_ridge_pred):
            self.time_model = rf_time
            time_pred = time_rf_pred
            best_time_name = "Random Forest"
        else:
            self.time_model = self.time_ridge
            time_pred = time_ridge_pred
            best_time_name = "Ridge Regression"

        # Evaluation results
        def metrics(y_true, y_pred, name):
            mae = float(mean_absolute_error(y_true, y_pred))
            rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
            r2 = float(r2_score(y_true, y_pred))
            print(f"  {name}: MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}")
            return {"mae": round(mae, 2), "rmse": round(rmse, 2), "r2": round(r2, 4)}

        cost_ridge_metrics = metrics(y_cost_test, cost_ridge_pred, "Cost Ridge")
        cost_rf_metrics = metrics(y_cost_test, cost_rf_pred, "Cost RF")
        time_ridge_metrics = metrics(y_time_test, time_ridge_pred, "Time Ridge")
        time_rf_metrics = metrics(y_time_test, time_rf_pred, "Time RF")

        # Store actual vs predicted for charts (sample 50 points)
        n_sample = min(50, len(y_cost_test))
        idx = np.random.choice(len(y_cost_test), n_sample, replace=False)
        self.actual_vs_predicted_cost = [
            {"actual": float(list(y_cost_test)[i]), "predicted": float(cost_pred[i])}
            for i in idx
        ]
        self.actual_vs_predicted_time = [
            {"actual": float(list(y_time_test)[i]), "predicted": float(time_pred[i])}
            for i in idx
        ]

        self.evaluation_results = {
            "cost_estimation": {
                "best_model": best_cost_name,
                "ridge_regression": cost_ridge_metrics,
                "random_forest": cost_rf_metrics,
                "actual_vs_predicted": self.actual_vs_predicted_cost,
            },
            "time_estimation": {
                "best_model": best_time_name,
                "ridge_regression": time_ridge_metrics,
                "random_forest": time_rf_metrics,
                "actual_vs_predicted": self.actual_vs_predicted_time,
            },
        }

        joblib.dump(self, MODELS_DIR / "regressor.pkl")
        joblib.dump(self.evaluation_results, MODELS_DIR / "regression_results.pkl")
        return self

    def predict_cost(self, days, group_size, base_cost_per_day, hotel_type, transport):
        """Predict total trip cost."""
        if self.cost_model is None:
            # Fallback formula
            mult = {"Budget": 0.7, "Standard": 1.0, "Luxury": 1.8}.get(hotel_type, 1.0)
            t_cost = {"Public Transport": 500, "Cab": 1500, "Rental": 2000, "Mixed": 1000}.get(transport, 1000)
            return int(base_cost_per_day * mult * days * group_size + t_cost * days + days * 600)

        row = self._build_reg_row(days, group_size, base_cost_per_day, hotel_type, transport)
        X = pd.DataFrame([row])[self.feature_names]

        if isinstance(self.cost_model, Ridge):
            X_s = self.scaler.transform(X)
            pred = self.cost_model.predict(X_s)[0]
        else:
            pred = self.cost_model.predict(X)[0]
        return max(int(pred), 500)

    def predict_time(self, days, group_size, base_cost_per_day, hotel_type, transport):
        """Predict total trip time (hours)."""
        if self.time_model is None:
            return days * 7.0

        row = self._build_reg_row(days, group_size, base_cost_per_day, hotel_type, transport)
        X = pd.DataFrame([row])[self.feature_names]

        if isinstance(self.time_model, Ridge):
            X_s = self.scaler.transform(X)
            pred = self.time_model.predict(X_s)[0]
        else:
            pred = self.time_model.predict(X)[0]
        return max(float(pred), 1.0)

    def _build_reg_row(self, days, group_size, base_cost_per_day, hotel_type, transport):
        mult_map = {"Budget": 0.7, "Standard": 1.0, "Luxury": 1.8}
        all_hotels = ["Budget", "Standard", "Luxury"]
        all_transports = ["Public Transport", "Cab", "Rental", "Mixed"]

        row = {
            "days": days,
            "group_size": group_size,
            "base_cost_per_day": base_cost_per_day,
            "cost_multiplier": mult_map.get(hotel_type, 1.0),
        }
        for h in all_hotels:
            row[f"hotel_{h}"] = 1 if hotel_type == h else 0
        for t in all_transports:
            row[f"transport_{t}"] = 1 if transport == t else 0
            row[f"transport_{t.replace(' ', '_')}"] = 1 if transport == t else 0
        return row

    @classmethod
    def load(cls):
        path = MODELS_DIR / "regressor.pkl"
        if path.exists():
            return joblib.load(path)
        return cls()
