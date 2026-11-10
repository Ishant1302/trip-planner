"""
ML Service - orchestrates the full ML pipeline for trip generation.
Loads trained models and executes: Classification → Clustering → Recommendation → Regression → Constraint Checking
"""

import pandas as pd
import numpy as np
import joblib
import json
import math
from pathlib import Path
from typing import Dict, List, Any, Optional

MODELS_DIR = Path(__file__).parent.parent.parent / "saved_models"
DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"


def _load_model(filename: str):
    path = MODELS_DIR / filename
    if path.exists():
        return joblib.load(path)
    return None


def _get_places_df(destination: str = None) -> pd.DataFrame:
    path = DATASETS_DIR / "places.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if destination:
        filtered = df[df["destination"].str.lower() == destination.lower()]
        if not filtered.empty:
            return filtered
    return df


def _get_destinations_df() -> pd.DataFrame:
    path = DATASETS_DIR / "destinations.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def run_ml_pipeline(user_input: dict) -> dict:
    """
    Full ML pipeline:
    1. Classification (RF) - predict like probability per place
    2. Clustering (K-Means) - assign traveller profile
    3. Recommendation - rank places by composite score
    4. Regression - estimate cost and time
    5. Constraint checking - adjust plan to fit budget/time
    6. Build itinerary
    """

    destination = user_input.get("destination", "")

    # --- Load models ---
    classifier = _load_model("trip_classifier.pkl")
    clusterer = _load_model("clusterer.pkl")
    regressor = _load_model("regressor.pkl")
    scaler = _load_model("scaler.pkl")

    # Feature names for classification
    feature_names = [
        "nature_interest","adventure_interest","food_interest",
        "history_interest","shopping_interest","culture_interest",
        "nature_score","adventure_score","food_score",
        "history_score","shopping_score","culture_score",
        "average_cost","time_needed","rating",
        "interest_match","cost_to_budget_ratio","rating_normalized",
        "avg_interest","walking_comfort_num","distance_from_city_centre",
    ]
    if classifier and hasattr(classifier, 'feature_names'):
        feature_names = classifier.feature_names

    # --- Step 1: Clustering - identify traveller profile ---
    cluster_result = {"label": "Adventure Traveller", "description": "Loves exploring", "cluster_id": 0}
    if clusterer:
        try:
            cluster_features = {
                "nature_interest": user_input.get("nature_interest", 3),
                "adventure_interest": user_input.get("adventure_interest", 3),
                "food_interest": user_input.get("food_interest", 3),
                "history_interest": user_input.get("history_interest", 3),
                "shopping_interest": user_input.get("shopping_interest", 3),
                "culture_interest": user_input.get("culture_interest", 3),
                "budget_normalized": min(user_input.get("budget", 15000) / 150000, 1),
                "days_normalized": min(user_input.get("days", 3) / 10, 1),
                "group_size_normalized": min(user_input.get("group_size", 1) / 8, 1),
                "walking_comfort_num": {"Low": 0, "Medium": 0.5, "High": 1.0}.get(
                    user_input.get("walking_comfort", "Medium"), 0.5
                ),
            }
            cluster_cols = ["nature_interest","adventure_interest","food_interest",
                           "history_interest","shopping_interest","culture_interest",
                           "budget_normalized","days_normalized","group_size_normalized","walking_comfort_num"]
            cluster_result = clusterer.predict_cluster(cluster_features, cluster_cols)
        except Exception as e:
            print(f"Clustering error: {e}")

    # --- Step 2: Get places and score ---
    places_df = _get_places_df(destination)
    if places_df.empty:
        return {"error": "No places data available. Please ensure datasets are generated."}

    # --- Step 3: Recommendation (uses classifier internally) ---
    from app.ml.recommendation import RecommendationEngine
    engine = RecommendationEngine(
        classifier=classifier,
        scaler=scaler,
        feature_names=feature_names,
    )

    recommended = engine.recommend_places(user_input, places_df, destination, top_n=20)

    # Apply walking comfort filter
    comfort = user_input.get("walking_comfort", "Medium")
    max_dist = {"Low": 15, "Medium": 40, "High": 999}.get(comfort, 40)
    recommended = [p for p in recommended if p.get("distance_from_city_centre", 0) <= max_dist]
    if not recommended:
        recommended = engine.recommend_places(user_input, places_df, destination, top_n=20)[:10]

    # --- Step 4: Regression - estimate cost/time ---
    dest_df = _get_destinations_df()
    dest_info = {}
    if not dest_df.empty:
        dest_row = dest_df[dest_df["destination"].str.lower() == destination.lower()]
        if not dest_row.empty:
            dest_info = dest_row.iloc[0].to_dict()

    base_cost_per_day = float(dest_info.get("avg_cost_per_day", 3000))
    days = int(user_input.get("days", 3))
    group_size = int(user_input.get("group_size", 1))
    hotel_type = user_input.get("accommodation_type", "Standard")
    transport = user_input.get("transport_preference", "Mixed")

    reg_cost = None
    reg_time = None
    if regressor:
        try:
            reg_cost = regressor.predict_cost(days, group_size, base_cost_per_day, hotel_type, transport)
            reg_time = regressor.predict_time(days, group_size, base_cost_per_day, hotel_type, transport)
        except Exception as e:
            print(f"Regression error: {e}")

    # --- Step 5: Constraint checking ---
    from app.ml.constraint_checker import ConstraintChecker
    checker = ConstraintChecker()
    user_input_cc = {**user_input, "avg_cost_per_day": base_cost_per_day}
    adjusted_places, constraint_report = checker.check_and_adjust(
        user_input_cc, recommended, regressor
    )

    # --- Step 6: Build day-wise itinerary ---
    itinerary = build_itinerary(adjusted_places, days, user_input)

    # --- Compile final result ---
    total_cost = constraint_report["total_estimated_cost"]
    if reg_cost:
        # Blend regression and constraint checker estimates
        total_cost = int(0.6 * reg_cost + 0.4 * constraint_report["total_estimated_cost"])

    budget = user_input.get("budget", 15000)
    budget_remaining = max(0, budget - total_cost)

    # Build recommendation cards (top 10)
    recommendation_cards = []
    for p in adjusted_places[:10]:
        recommendation_cards.append({
            "place_id": int(p.get("place_id", 0)),
            "place_name": str(p.get("place_name", "")),
            "destination": str(p.get("destination", destination)),
            "category": str(p.get("category", "")),
            "rating": float(p.get("rating", 4.0)),
            "average_cost": int(p.get("average_cost", 0)),
            "time_needed": float(p.get("time_needed", 1)),
            "image": str(p.get("image", "")),
            "description": str(p.get("description", f"{p.get('category', 'Popular')} attraction in {destination}")),
            "rf_probability": float(p.get("rf_probability", 0.5)),
            "like_probability_pct": str(p.get("like_probability_pct", "50%")),
            "composite_score": float(p.get("composite_score", 0)),
            "interest_match": float(p.get("interest_match", 0)),
            "budget_fit": float(p.get("budget_fit", 0)),
            "reasons": list(p.get("reasons", [])),
            "location": str(p.get("location", "")),
            "distance_from_city_centre": float(p.get("distance_from_city_centre", 0)),
        })

    result = {
        "destination": destination,
        "destination_info": {
            "image": str(dest_info.get("image", "")),
            "description": str(dest_info.get("description", "")),
            "avg_cost_per_day": base_cost_per_day,
        },
        "days": days,
        "group_size": group_size,
        "budget": budget,
        "traveller_profile": cluster_result,
        "total_estimated_cost": total_cost,
        "cost_per_person": int(total_cost / max(group_size, 1)),
        "daily_cost": int(total_cost / max(days, 1)),
        "budget_remaining": budget_remaining,
        "over_budget": total_cost > budget,
        "regression_cost_estimate": reg_cost,
        "regression_time_estimate": reg_time,
        "budget_breakdown": constraint_report["budget_breakdown"],
        "recommendations": recommendation_cards,
        "itinerary": itinerary,
        "constraint_report": {
            "violations": constraint_report["violations"],
            "adjustments": constraint_report["adjustments"],
            "total_activity_hours": constraint_report["total_activity_time_hours"],
            "available_time_hours": constraint_report["available_time_hours"],
        },
        "ml_insights": {
            "traveller_profile": cluster_result.get("label", ""),
            "cluster_description": cluster_result.get("description", ""),
            "avg_rf_probability": round(
                sum(p.get("rf_probability", 0.5) for p in adjusted_places[:10]) /
                max(len(adjusted_places[:10]), 1), 4
            ),
            "avg_recommendation_score": round(
                sum(p.get("composite_score", 0) for p in adjusted_places[:10]) /
                max(len(adjusted_places[:10]), 1), 4
            ),
            "top_place_probability": round(
                adjusted_places[0].get("rf_probability", 0.5) if adjusted_places else 0.5, 4
            ),
            "models_used": ["Random Forest Classifier", "K-Means Clustering",
                           "Recommendation Engine", "Ridge/RF Regression",
                           "Constraint Checker"],
        }
    }

    return result


def build_itinerary(places: list, days: int, user_input: dict) -> dict:
    """Distribute places evenly across days, guaranteeing every day has curated activities."""
    destination = user_input.get("destination", "the Destination")
    pace = user_input.get("trip_pace", "Balanced")

    sorted_places = sorted(places, key=lambda p: p.get("composite_score", 0), reverse=True)
    total_places = len(sorted_places)

    day_themes = [
        "Iconic Landmarks & Historical Heritage",
        "Scenic Nature, Viewpoints & Photo Spots",
        "Cultural Discovery, Arts & Local Markets",
        "Hidden Gems, Architecture & Culinary Walk",
        "Outdoor Adventures & Scenic Escapes",
        "Traditional Bazaars & Sunset Leisure",
        "Spiritual Shrines & Local Delicacies"
    ]

    time_slots = [
        {"slot": "Morning", "time": "09:30 AM – 12:30 PM"},
        {"slot": "Afternoon", "time": "01:30 PM – 04:30 PM"},
        {"slot": "Evening", "time": "05:30 PM – 08:30 PM"},
    ]

    day_plan = {}

    if total_places == 0:
        for day in range(1, days + 1):
            day_plan[str(day)] = {
                "day": day,
                "title": f"Day {day} – Exploring {destination}",
                "day_title": f"Day {day} – Exploring {destination}",
                "places": [],
                "total_cost": 0,
                "total_time": 0,
            }
        return day_plan

    # Distribute places round-robin across days so EVERY day has activities
    day_buckets = [[] for _ in range(days)]
    for idx, place in enumerate(sorted_places):
        day_idx = idx % days
        day_buckets[day_idx].append(place)

    for day in range(1, days + 1):
        raw_day_places = day_buckets[day - 1]

        # If a day ended up empty (e.g. fewer places than days), cycle from top places
        if not raw_day_places and sorted_places:
            cycle_place = sorted_places[(day - 1) % len(sorted_places)]
            raw_day_places = [cycle_place]

        day_places = []
        for slot_idx, p in enumerate(raw_day_places[:3]):  # max 3 per day
            slot_info = time_slots[slot_idx % len(time_slots)]
            description = p.get("description") or f"Explore {p.get('place_name', 'this attraction')}, known for its {p.get('category', 'popular')} experience in {destination}."
            day_places.append({
                **{k: v for k, v in p.items() if k not in ["reasons"]},
                "time_of_day": slot_info["slot"],
                "time_slot": slot_info["time"],
                "day": day,
                "description": description,
                "reasons": p.get("reasons", []),
            })

        theme = day_themes[(day - 1) % len(day_themes)]
        day_title = f"Day {day} – {theme}"

        day_plan[str(day)] = {
            "day": day,
            "title": day_title,
            "day_title": day_title,
            "places": day_places,
            "total_cost": sum(int(p.get("average_cost", 0)) for p in day_places),
            "total_time": sum(float(p.get("time_needed", 1)) for p in day_places),
        }

    return day_plan
