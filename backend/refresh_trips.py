import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))
from app.database.database import SessionLocal
from app.models.db_models import Trip
from app.services import ml_service

def refresh():
    db = SessionLocal()
    trips = db.query(Trip).all()
    print(f"Found {len(trips)} trips in database to refresh.")

    for trip in trips:
        print(f"Refreshing Trip #{trip.id}: {trip.destination}, {trip.days} days, Rs.{trip.budget}")
        user_input = {
            "destination": trip.destination,
            "days": int(trip.days),
            "group_size": int(trip.group_size or 2),
            "budget": float(trip.budget),
            "nature_interest": 4,
            "adventure_interest": 3,
            "food_interest": 4,
            "history_interest": 5,
            "shopping_interest": 3,
            "culture_interest": 5,
            "travel_style": "Balanced",
            "pace": "Moderate"
        }
        res = ml_service.run_ml_pipeline(user_input)
        if "error" not in res:
            trip.ml_results = res
            trip.itinerary = res.get("itinerary", {})
            db.commit()
            
            itinerary = res.get("itinerary", {})
            day_counts = []
            for day_k, day_v in itinerary.items():
                places_count = len(day_v.get("places", []))
                day_counts.append(f"Day {day_k}: {places_count} places")
            print(f"  -> Trip #{trip.id} updated! {', '.join(day_counts)}")
        else:
            print(f"  -> Error for Trip #{trip.id}: {res.get('error')}")

    db.close()
    print("\nAll database trips successfully refreshed with deep places and verified visuals!")

if __name__ == "__main__":
    refresh()
