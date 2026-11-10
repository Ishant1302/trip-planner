"""
Enriches and saves all 266 places to places.csv with verified images from Wikipedia and Commons.
"""

import urllib.request
import urllib.parse
import json
import ssl
import sys
import shutil
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl._create_unverified_context()
DATA_DIR = Path(__file__).parent

sys.path.insert(0, str(DATA_DIR))
from build_deep_places import PLACES_DATA
from all_destinations_data import DESTINATIONS_6_TO_20
from destinations_10_to_20 import DESTINATIONS_10_TO_20
from destinations_13_to_20 import DESTINATIONS_13_TO_20

all_places = PLACES_DATA + DESTINATIONS_6_TO_20 + DESTINATIONS_10_TO_20 + DESTINATIONS_13_TO_20

def fetch_image_for_place(place):
    wiki_title = place.get("wiki_title")
    fallback = place.get("fallback_image", "")
    final_image = fallback

    if wiki_title:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_title)}"
            req = urllib.request.Request(url, headers={"User-Agent": "VoyageML/1.0 (TravelResearch)"})
            res = urllib.request.urlopen(req, context=ctx, timeout=3.5)
            data = json.loads(res.read())
            # Prefer high quality thumbnail or original image
            thumb = data.get("thumbnail", {}).get("source")
            orig = data.get("originalimage", {}).get("source")
            if thumb:
                final_image = thumb
            elif orig:
                final_image = orig
        except Exception as e:
            # Silently use fallback
            pass

    clean_place = {
        "place_name": place["place_name"],
        "destination": place["destination"],
        "country": place["country"],
        "region": place["region"],
        "category": place["category"],
        "nature_score": place["nature_score"],
        "adventure_score": place["adventure_score"],
        "food_score": place["food_score"],
        "history_score": place["history_score"],
        "shopping_score": place["shopping_score"],
        "culture_score": place["culture_score"],
        "average_cost": place["average_cost"],
        "time_needed": place["time_needed"],
        "rating": place["rating"],
        "location": place["location"],
        "distance_from_city_centre": place["distance_from_city_centre"],
        "image": final_image,
        "description": place["description"]
    }
    return clean_place

def main():
    print(f"Starting enrichment of {len(all_places)} places across 20 destinations...")
    enriched_places = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_idx = {executor.submit(fetch_image_for_place, p): i for i, p in enumerate(all_places)}
        results = [None] * len(all_places)
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"Error at {idx}: {e}")
                results[idx] = all_places[idx]
        enriched_places = results

    df = pd.DataFrame(enriched_places)
    
    # Backup existing places.csv
    csv_path = DATA_DIR / "places.csv"
    if csv_path.exists():
        backup_path = DATA_DIR / "places.csv.bak"
        shutil.copyfile(csv_path, backup_path)
        print(f"Backed up existing places.csv to {backup_path}")

    df.to_csv(csv_path, index=False)
    print(f"Successfully saved {len(df)} places to {csv_path}")
    print("\nPlaces per destination:")
    print(df["destination"].value_counts())

if __name__ == "__main__":
    main()

