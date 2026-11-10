"""
Classification Module - Random Forest Classifier
Predicts whether a user will Like or Not Like a place.
Compares: Logistic Regression, Decision Tree, Random Forest
Final model: Random Forest (best F1-score)
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, roc_auc_score, confusion_matrix,
                              classification_report)
import joblib
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "saved_models"


class TripClassifier:
    """Random Forest classifier to predict user-place preference."""

    def __init__(self):
        self.rf_model = None
        self.lr_model = None
        self.dt_model = None
        self.best_model = None
        self.feature_names = []
        self.model_comparison = {}
        self.evaluation_results = {}
        self.feature_importance_data = []

    def train_all_models(self, X_train, y_train, feature_names):
        """Train and compare Logistic Regression, Decision Tree, Random Forest."""
        self.feature_names = list(feature_names)

        print("Training Logistic Regression...")
        self.lr_model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
        self.lr_model.fit(X_train, y_train)

        print("Training Decision Tree...")
        self.dt_model = DecisionTreeClassifier(
            max_depth=8, min_samples_leaf=5, random_state=42
        )
        self.dt_model.fit(X_train, y_train)

        print("Training Random Forest with GridSearchCV...")
        rf_param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [8, 12, None],
            'min_samples_leaf': [2, 5],
        }
        rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
        grid_search = GridSearchCV(
            rf_base, rf_param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=0
        )
        grid_search.fit(X_train, y_train)
        self.rf_model = grid_search.best_estimator_
        print(f"Best RF params: {grid_search.best_params_}")

        # Cross-val scores
        self.cv_scores = cross_val_score(self.rf_model, X_train, y_train, cv=5, scoring='f1')
        print(f"RF CV F1: {self.cv_scores.mean():.4f} +/- {self.cv_scores.std():.4f}")

        self.best_model = self.rf_model  # RF is the final model per report
        self._save_models()
        return self

    def evaluate(self, X_test, y_test):
        """Evaluate all three models on test set."""
        results = {}
        for name, model in [("Logistic Regression", self.lr_model),
                              ("Decision Tree", self.dt_model),
                              ("Random Forest", self.rf_model)]:
            if model is None:
                continue
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred

            results[name] = {
                "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
                "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
                "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
                "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            }
            print(f"\n{name}: Acc={results[name]['accuracy']:.4f} F1={results[name]['f1_score']:.4f}")

        self.model_comparison = results

        # Feature importance for RF
        if self.rf_model is not None:
            importances = self.rf_model.feature_importances_
            fi_data = sorted(
                [{"feature": f, "importance": round(float(imp), 4)}
                 for f, imp in zip(self.feature_names, importances)],
                key=lambda x: x["importance"], reverse=True
            )
            self.feature_importance_data = fi_data

        # Determine best model
        best_name = max(results, key=lambda k: results[k]["f1_score"])
        self.evaluation_results = {
            "model_comparison": results,
            "best_model": best_name,
            "final_model": "Random Forest",
            "feature_importance": self.feature_importance_data,
            "cv_f1_mean": round(float(self.cv_scores.mean()), 4) if hasattr(self, 'cv_scores') else 0,
            "cv_f1_std": round(float(self.cv_scores.std()), 4) if hasattr(self, 'cv_scores') else 0,
        }

        joblib.dump(self.evaluation_results, MODELS_DIR / "classification_results.pkl")
        return self.evaluation_results

    def predict_like_probability(self, user_features: dict, place_features: dict,
                                  feature_names: list, scaler) -> float:
        """
        Predict the probability that a user will like a specific place.
        Returns a float between 0 and 1.
        """
        if self.rf_model is None:
            return 0.5  # fallback

        interest_map = {
            "Nature": "nature_interest", "Adventure": "adventure_interest",
            "Food": "food_interest", "History": "history_interest",
            "Shopping": "shopping_interest", "Culture": "culture_interest",
        }
        score_map = {
            "Nature": "nature_score", "Adventure": "adventure_score",
            "Food": "food_score", "History": "history_score",
            "Shopping": "shopping_score", "Culture": "culture_score",
        }
        wc_map = {"Low": 0, "Medium": 0.5, "High": 1.0}

        cat = place_features.get("category", "Nature")
        icol = interest_map.get(cat, "nature_interest")
        scol = score_map.get(cat, "nature_score")
        user_interest = user_features.get(icol, 3)
        place_score = place_features.get(scol, 3)
        interest_match = (user_interest + place_score) / 10.0

        budget = user_features.get("budget", 15000)
        days = user_features.get("days", 3)
        avg_cost = place_features.get("average_cost", 500)
        cost_ratio = avg_cost / (budget / max(days, 1) + 1)

        walking_comfort = user_features.get("walking_comfort", "Medium")
        wc_num = wc_map.get(walking_comfort, 0.5)

        avg_interest = (
            user_features.get("nature_interest", 3) +
            user_features.get("adventure_interest", 3) +
            user_features.get("food_interest", 3) +
            user_features.get("history_interest", 3) +
            user_features.get("shopping_interest", 3) +
            user_features.get("culture_interest", 3)
        ) / 30.0

        row = {
            "nature_interest": user_features.get("nature_interest", 3),
            "adventure_interest": user_features.get("adventure_interest", 3),
            "food_interest": user_features.get("food_interest", 3),
            "history_interest": user_features.get("history_interest", 3),
            "shopping_interest": user_features.get("shopping_interest", 3),
            "culture_interest": user_features.get("culture_interest", 3),
            "nature_score": place_features.get("nature_score", 3),
            "adventure_score": place_features.get("adventure_score", 3),
            "food_score": place_features.get("food_score", 3),
            "history_score": place_features.get("history_score", 3),
            "shopping_score": place_features.get("shopping_score", 3),
            "culture_score": place_features.get("culture_score", 3),
            "average_cost": avg_cost,
            "time_needed": place_features.get("time_needed", 2),
            "rating": place_features.get("rating", 4.0),
            "interest_match": interest_match,
            "cost_to_budget_ratio": cost_ratio,
            "rating_normalized": place_features.get("rating", 4.0) / 5.0,
            "avg_interest": avg_interest,
            "walking_comfort_num": wc_num,
            "distance_from_city_centre": place_features.get("distance_from_city_centre", 10),
        }

        X = pd.DataFrame([row])[feature_names]
        X_scaled = scaler.transform(X)
        prob = self.rf_model.predict_proba(X_scaled)[0][1]
        return float(prob)

    def _save_models(self):
        MODELS_DIR.mkdir(exist_ok=True)
        joblib.dump(self.rf_model, MODELS_DIR / "rf_classifier.pkl")
        joblib.dump(self.lr_model, MODELS_DIR / "lr_classifier.pkl")
        joblib.dump(self.dt_model, MODELS_DIR / "dt_classifier.pkl")
        joblib.dump(self, MODELS_DIR / "trip_classifier.pkl")
        print("Models saved.")

    @classmethod
    def load(cls):
        path = MODELS_DIR / "trip_classifier.pkl"
        if path.exists():
            return joblib.load(path)
        return cls()
