"""Data service - loads destination and places data from CSVs."""

import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Optional

DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"


def get_all_destinations(search: str = None, category: str = None,
                          min_rating: float = None, max_budget: float = None,
                          sort_by: str = "avg_rating") -> List[dict]:
    path = DATASETS_DIR / "destinations.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)

    if search:
        mask = (df["destination"].str.lower().str.contains(search.lower()) |
                df["country"].str.lower().str.contains(search.lower()))
        df = df[mask]

    if min_rating:
        df = df[df["avg_rating"] >= min_rating]

    if max_budget:
        df = df[df["avg_cost_per_day"] <= max_budget]

    if category:
        df = df[df["categories"].str.contains(category, na=False)]

    if sort_by == "avg_rating":
        df = df.sort_values("avg_rating", ascending=False)
    elif sort_by == "avg_cost_per_day":
        df = df.sort_values("avg_cost_per_day")
    elif sort_by == "best_duration_days":
        df = df.sort_values("best_duration_days")

    results = []
    for _, row in df.iterrows():
        d = row.to_dict()
        # Parse categories JSON
        try:
            d["categories"] = json.loads(d["categories"]) if isinstance(d["categories"], str) else d["categories"]
        except Exception:
            d["categories"] = []
        results.append(d)
    return results


def get_destination_by_name(name: str) -> Optional[dict]:
    destinations = get_all_destinations()
    for d in destinations:
        if d["destination"].lower() == name.lower():
            return d
    return None


def get_places_for_destination(destination: str) -> List[dict]:
    path = DATASETS_DIR / "places.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    filtered = df[df["destination"].str.lower() == destination.lower()]
    return filtered.to_dict("records")


def get_all_places(destination: str = None, search: str = None) -> List[dict]:
    path = DATASETS_DIR / "places.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    if destination:
        df = df[df["destination"].str.strip().str.lower() == destination.strip().lower()]
    if search:
        s = search.strip().lower()
        df = df[df["place_name"].str.lower().str.contains(s) | df["category"].str.lower().str.contains(s)]
    return df.to_dict("records")


def update_place_image(place_name: str, image_url: str, destination: Optional[str] = None) -> bool:
    """Updates the image for a place in places.csv."""
    path = DATASETS_DIR / "places.csv"
    if not path.exists():
        return False
    df = pd.read_csv(path)
    
    if destination:
        mask = (df["place_name"].str.strip().str.lower() == place_name.strip().lower()) & \
               (df["destination"].str.strip().str.lower() == destination.strip().lower())
    else:
        mask = df["place_name"].str.strip().str.lower() == place_name.strip().lower()
        
    if not df[mask].empty:
        df.loc[mask, "image"] = image_url.strip()
        df.to_csv(path, index=False)
        return True
    return False


def update_destination_image(destination: str, image_url: str) -> bool:
    """Updates the hero image for a destination in destinations.csv."""
    path = DATASETS_DIR / "destinations.csv"
    if not path.exists():
        return False
    df = pd.read_csv(path)
    mask = df["destination"].str.strip().str.lower() == destination.strip().lower()
    if not df[mask].empty:
        df.loc[mask, "image"] = image_url.strip()
        df.to_csv(path, index=False)
        return True
    return False
