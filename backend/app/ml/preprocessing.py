"""
Data Preprocessing Pipeline for Trip Planner ML System
Handles loading, cleaning, feature engineering and splitting datasets.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')

DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "saved_models"
MODELS_DIR.mkdir(exist_ok=True)


class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.is_fitted = False

    def load_datasets(self):
        """Load all CSV datasets."""
        places = pd.read_csv(DATASETS_DIR / "places.csv")
        users = pd.read_csv(DATASETS_DIR / "users.csv")
        interactions = pd.read_csv(DATASETS_DIR / "interactions.csv")
        past_trips = pd.read_csv(DATASETS_DIR / "past_trips.csv")
        destinations = pd.read_csv(DATASETS_DIR / "destinations.csv")
        return places, users, interactions, past_trips, destinations

    def clean_places(self, df):
        """Clean and validate places dataset."""
        df = df.drop_duplicates(subset=["place_id"])
        # Handle missing values
        numeric_cols = ["nature_score","adventure_score","food_score","history_score",
                        "shopping_score","culture_score","average_cost","time_needed","rating",
                        "distance_from_city_centre"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        # Clamp scores 1-5
        score_cols = ["nature_score","adventure_score","food_score","history_score","shopping_score","culture_score"]
        for col in score_cols:
            df[col] = df[col].clip(1, 5)
        # Fill categorical
        df["category"] = df["category"].fillna("Nature")
        df["destination"] = df["destination"].fillna("Unknown")
        return df

    def clean_users(self, df):
        """Clean and validate users dataset."""
        df = df.drop_duplicates(subset=["user_id"])
        numeric_cols = ["budget","days","group_size","nature_interest","adventure_interest",
                        "food_interest","history_interest","shopping_interest","culture_interest"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        interest_cols = ["nature_interest","adventure_interest","food_interest",
                         "history_interest","shopping_interest","culture_interest"]
        for col in interest_cols:
            df[col] = df[col].clip(1, 5)
        df["food_preference"] = df["food_preference"].fillna("No Preference")
        df["walking_comfort"] = df["walking_comfort"].fillna("Medium")
        return df

    def clean_interactions(self, df):
        df = df.drop_duplicates(subset=["user_id","place_id"])
        df["liked"] = df["liked"].fillna(0).astype(int)
        df["interaction"] = df["interaction"].fillna("Skipped")
        return df

    def clean_past_trips(self, df):
        df = df.drop_duplicates()
        numeric_cols = ["days","group_size","actual_cost","actual_time","base_cost_per_day"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        df["hotel_type"] = df["hotel_type"].fillna("Standard")
        df["transport"] = df["transport"].fillna("Mixed")
        return df

    def build_classification_features(self, users_df, places_df, interactions_df):
        """Build feature matrix for classification (like/not like)."""
        merged = interactions_df.merge(users_df, on="user_id", how="left")
        merged = merged.merge(places_df, on="place_id", how="left")

        interest_map = {
            "Nature": "nature_interest",
            "Adventure": "adventure_interest",
            "Food": "food_interest",
            "History": "history_interest",
            "Shopping": "shopping_interest",
            "Culture": "culture_interest",
        }
        score_map = {
            "Nature": "nature_score",
            "Adventure": "adventure_score",
            "Food": "food_score",
            "History": "history_score",
            "Shopping": "shopping_score",
            "Culture": "culture_score",
        }

        def get_interest_match(row):
            cat = row.get("category", "Nature")
            icol = interest_map.get(cat, "nature_interest")
            scol = score_map.get(cat, "nature_score")
            user_interest = row.get(icol, 3)
            place_score = row.get(scol, 3)
            return (user_interest + place_score) / 10.0  # normalize to 0-1

        merged["interest_match"] = merged.apply(get_interest_match, axis=1)
        merged["cost_to_budget_ratio"] = merged["average_cost"] / (merged["budget"] / merged["days"] + 1)
        merged["rating_normalized"] = merged["rating"] / 5.0
        merged["avg_interest"] = (merged["nature_interest"] + merged["adventure_interest"] +
                                   merged["food_interest"] + merged["history_interest"] +
                                   merged["shopping_interest"] + merged["culture_interest"]) / 30.0

        # Walking comfort encoding
        wc_map = {"Low": 0, "Medium": 0.5, "High": 1.0}
        merged["walking_comfort_num"] = merged["walking_comfort"].map(wc_map).fillna(0.5)

        feature_cols = [
            "nature_interest","adventure_interest","food_interest",
            "history_interest","shopping_interest","culture_interest",
            "nature_score","adventure_score","food_score",
            "history_score","shopping_score","culture_score",
            "average_cost","time_needed","rating",
            "interest_match","cost_to_budget_ratio","rating_normalized",
            "avg_interest","walking_comfort_num","distance_from_city_centre",
        ]
        feature_cols = [c for c in feature_cols if c in merged.columns]
        X = merged[feature_cols].fillna(0)
        y = merged["liked"].astype(int)
        self.feature_names = feature_cols
        return X, y, merged

    def build_clustering_features(self, users_df):
        """Build feature matrix for K-Means clustering."""
        budget_max = users_df["budget"].quantile(0.95)
        features = pd.DataFrame({
            "nature_interest": users_df["nature_interest"],
            "adventure_interest": users_df["adventure_interest"],
            "food_interest": users_df["food_interest"],
            "history_interest": users_df["history_interest"],
            "shopping_interest": users_df["shopping_interest"],
            "culture_interest": users_df["culture_interest"],
            "budget_normalized": (users_df["budget"] / budget_max).clip(0, 1),
            "days_normalized": (users_df["days"] / 10).clip(0, 1),
            "group_size_normalized": (users_df["group_size"] / 8).clip(0, 1),
            "walking_comfort_num": users_df["walking_comfort"].map({"Low":0,"Medium":0.5,"High":1.0}).fillna(0.5),
        })
        return features.fillna(0)

    def build_regression_features(self, past_trips_df):
        """Build features for regression (cost & time estimation)."""
        df = past_trips_df.copy()
        # One-hot encode categorical columns
        hotel_dummies = pd.get_dummies(df["hotel_type"], prefix="hotel")
        transport_dummies = pd.get_dummies(df["transport"], prefix="transport")

        features = pd.concat([
            df[["days","group_size","base_cost_per_day","cost_multiplier"]],
            hotel_dummies,
            transport_dummies,
        ], axis=1)

        y_cost = df["actual_cost"]
        y_time = df["actual_time"]
        return features.fillna(0), y_cost, y_time

    def scale_features(self, X, fit=True):
        """Scale numerical features."""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
            joblib.dump(self.scaler, MODELS_DIR / "scaler.pkl")
        else:
            X_scaled = self.scaler.transform(X)
        return pd.DataFrame(X_scaled, columns=X.columns if hasattr(X, 'columns') else None)

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """80/20 train-test split."""
        return train_test_split(X, y, test_size=test_size, random_state=random_state,
                                stratify=y if len(y.unique()) == 2 else None)

    def prepare_all(self):
        """Full preprocessing pipeline. Returns all prepared datasets."""
        places, users, interactions, past_trips, destinations = self.load_datasets()
        places = self.clean_places(places)
        users = self.clean_users(users)
        interactions = self.clean_interactions(interactions)
        past_trips = self.clean_past_trips(past_trips)

        # Classification
        X_clf, y_clf, merged = self.build_classification_features(users, places, interactions)
        X_clf_scaled = self.scale_features(X_clf, fit=True)
        X_train, X_test, y_train, y_test = self.split_data(X_clf_scaled, y_clf)

        # Clustering
        X_cluster = self.build_clustering_features(users)

        # Regression
        X_reg, y_cost, y_time = self.build_regression_features(past_trips)
        X_reg_train, X_reg_test, y_cost_train, y_cost_test = train_test_split(
            X_reg, y_cost, test_size=0.2, random_state=42
        )
        _, _, y_time_train, y_time_test = train_test_split(
            X_reg, y_time, test_size=0.2, random_state=42
        )

        self.is_fitted = True
        joblib.dump(self, MODELS_DIR / "preprocessor.pkl")

        return {
            "classification": {
                "X_train": X_train, "X_test": X_test,
                "y_train": y_train, "y_test": y_test,
                "feature_names": self.feature_names,
            },
            "clustering": {
                "X": X_cluster, "users_df": users,
            },
            "regression": {
                "X_train": X_reg_train, "X_test": X_reg_test,
                "y_cost_train": y_cost_train, "y_cost_test": y_cost_test,
                "y_time_train": y_time_train, "y_time_test": y_time_test,
            },
            "raw": {
                "places": places, "users": users,
                "interactions": interactions, "past_trips": past_trips,
                "destinations": destinations,
            }
        }


def load_preprocessor():
    """Load saved preprocessor."""
    path = MODELS_DIR / "preprocessor.pkl"
    if path.exists():
        return joblib.load(path)
    return DataPreprocessor()
