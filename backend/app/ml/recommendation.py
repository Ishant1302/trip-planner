"""
Recommendation Engine
Ranks destinations and places using:
1. Random Forest Like probability
2. Interest match score
3. Place rating
4. Budget fit score

Transparent weighted scoring with explanation generation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from typing import List, Dict, Any

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "saved_models"
DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"


class RecommendationEngine:
    """Weighted recommendation engine combining ML outputs."""

    # Weights for scoring (must sum to 1.0)
    WEIGHTS = {
        "rf_probability": 0.35,
        "interest_match": 0.30,
        "rating": 0.20,
        "budget_fit": 0.15,
    }

    def __init__(self, classifier=None, scaler=None, feature_names=None):
        self.classifier = classifier
        self.scaler = scaler
        self.feature_names = feature_names or []

    def compute_interest_match(self, user_features: dict, place: dict) -> float:
        """Compute normalized interest-to-place match score (0-1)."""
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
        cat = place.get("category", "Nature")
        icol = interest_map.get(cat, "nature_interest")
        scol = score_map.get(cat, "nature_score")

        user_interest = user_features.get(icol, 3)
        place_score = place.get(scol, 3)
        return float((user_interest + place_score) / 10.0)

    def compute_budget_fit(self, user_features: dict, place: dict) -> float:
        """Score how well a place fits the user's budget (0-1)."""
        budget = user_features.get("budget", 15000)
        days = max(user_features.get("days", 3), 1)
        group_size = max(user_features.get("group_size", 1), 1)
        avg_cost = place.get("average_cost", 500)

        budget_per_person = budget / group_size
        cost_per_day = avg_cost
        total_place_cost = cost_per_day * days

        if total_place_cost <= budget_per_person * 0.15:
            return 1.0
        elif total_place_cost <= budget_per_person * 0.25:
            return 0.8
        elif total_place_cost <= budget_per_person * 0.40:
            return 0.6
        elif total_place_cost <= budget_per_person * 0.60:
            return 0.4
        else:
            return 0.2

    def score_place(self, user_features: dict, place: dict) -> dict:
        """Compute composite recommendation score for a place."""
        # 1. RF probability
        if self.classifier and self.scaler and self.feature_names:
            rf_prob = self.classifier.predict_like_probability(
                user_features, place, self.feature_names, self.scaler
            )
        else:
            rf_prob = 0.5

        # 2. Interest match
        interest_match = self.compute_interest_match(user_features, place)

        # 3. Rating score (normalized)
        rating_score = float(place.get("rating", 4.0)) / 5.0

        # 4. Budget fit
        budget_fit = self.compute_budget_fit(user_features, place)

        # Weighted composite
        composite = (
            self.WEIGHTS["rf_probability"] * rf_prob +
            self.WEIGHTS["interest_match"] * interest_match +
            self.WEIGHTS["rating"] * rating_score +
            self.WEIGHTS["budget_fit"] * budget_fit
        )

        # Generate explanation
        reasons = []
        if rf_prob >= 0.7:
            reasons.append(f"High ML predicted preference ({rf_prob*100:.0f}%)")
        elif rf_prob >= 0.5:
            reasons.append(f"Good ML predicted preference ({rf_prob*100:.0f}%)")

        cat = place.get("category", "Nature")
        icol_name = cat.lower() + " interest"
        icol = cat.lower() + "_interest"
        user_int = user_features.get(icol, 3)
        if interest_match >= 0.7:
            reasons.append(f"Strong match for your {icol_name} (rated {user_int}/5)")
        elif interest_match >= 0.5:
            reasons.append(f"Matches your {icol_name}")

        rating = place.get("rating", 4.0)
        if rating >= 4.5:
            reasons.append(f"Excellent visitor rating ({rating} stars)")
        elif rating >= 4.0:
            reasons.append(f"Good visitor rating ({rating} stars)")

        if budget_fit >= 0.8:
            reasons.append("Well within your budget")
        elif budget_fit >= 0.6:
            reasons.append("Fits your budget comfortably")

        if not reasons:
            reasons.append("Recommended based on your travel profile")

        return {
            "rf_probability": round(rf_prob, 4),
            "interest_match": round(interest_match, 4),
            "rating_score": round(rating_score, 4),
            "budget_fit": round(budget_fit, 4),
            "composite_score": round(composite, 4),
            "reasons": reasons,
        }

    def recommend_places(self, user_features: dict, places_df: pd.DataFrame,
                          destination: str = None, top_n: int = 15) -> List[Dict]:
        """Recommend top-N places, filtered by destination if given."""
        df = places_df.copy()
        if destination:
            df = df[df["destination"].str.lower() == destination.lower()]
        if df.empty:
            df = places_df.copy()

        results = []
        for _, row in df.iterrows():
            place = row.to_dict()
            scores = self.score_place(user_features, place)
            results.append({
                **place,
                **scores,
                "like_probability_pct": f"{scores['rf_probability']*100:.0f}%",
            })

        results.sort(key=lambda x: x["composite_score"], reverse=True)
        return results[:top_n]

    def check_food_preference(self, user_features: dict, place: dict) -> bool:
        """Check if food preference is compatible (simple heuristic)."""
        food_pref = user_features.get("food_preference", "No Preference")
        if food_pref == "No Preference":
            return True
        cat = place.get("category", "")
        if cat == "Food":
            return True  # Always include food places — user can choose
        return True  # Non-food places are always compatible

    def filter_by_walking_comfort(self, user_features: dict, places: List[Dict]) -> List[Dict]:
        """Filter high-distance places for low walking comfort users."""
        comfort = user_features.get("walking_comfort", "Medium")
        if comfort == "Low":
            return [p for p in places if p.get("distance_from_city_centre", 0) <= 15]
        elif comfort == "Medium":
            return [p for p in places if p.get("distance_from_city_centre", 0) <= 40]
        return places
