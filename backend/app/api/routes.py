"""FastAPI route definitions."""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List, Optional
import json
import base64
import re
from pathlib import Path
from datetime import datetime

from app.database.database import get_db
from app.models.db_models import Trip, Favourite
from app.schemas.schemas import (
    TripGenerateRequest, TripCreate, TripUpdate, TripResponse,
    FavouriteCreate, FavouriteResponse, PlaceImageUpdate, DestinationImageUpdate,
    ImageUploadPayload
)
from app.services import data_service, ml_service
from app.ml import evaluation

router = APIRouter()


# ─── Health ───────────────────────────────────────────────────────────────────

@router.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# ─── Destinations ─────────────────────────────────────────────────────────────

@router.get("/destinations")
def list_destinations(
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_budget: Optional[float] = None,
    sort_by: str = "avg_rating",
):
    destinations = data_service.get_all_destinations(search, category, min_rating, max_budget, sort_by)
    return {"destinations": destinations, "total": len(destinations)}


@router.get("/destinations/names")
def get_destination_names():
    destinations = data_service.get_all_destinations()
    return {"names": [d["destination"] for d in destinations]}


@router.get("/destinations/{name}")
def get_destination(name: str):
    dest = data_service.get_destination_by_name(name)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    places = data_service.get_places_for_destination(name)
    return {"destination": dest, "places": places}


# ─── Places & Image Editing ───────────────────────────────────────────────────

@router.get("/places")
def list_places(destination: Optional[str] = None, search: Optional[str] = None):
    places = data_service.get_all_places(destination=destination, search=search)
    return {"places": places, "total": len(places)}


@router.put("/places/image")
def update_place_image_endpoint(payload: PlaceImageUpdate, db: Session = Depends(get_db)):
    """Allows user to customize/edit the image URL for any place."""
    success = data_service.update_place_image(
        place_name=payload.place_name,
        image_url=payload.image_url,
        destination=payload.destination
    )
    if not success:
        raise HTTPException(status_code=404, detail=f"Place '{payload.place_name}' not found")
    
    # Update image in any active trip itineraries in database
    trips = db.query(Trip).all()
    updated_trips = 0
    for trip in trips:
        itinerary = trip.itinerary
        if not itinerary:
            continue
        modified = False
        # If stored as string, decode
        if isinstance(itinerary, str):
            try:
                itinerary = json.loads(itinerary)
            except Exception:
                continue
        
        if isinstance(itinerary, dict):
            for day_data in itinerary.values():
                for place in day_data.get("places", []):
                    if place.get("place_name", "").strip().lower() == payload.place_name.strip().lower():
                        place["image"] = payload.image_url.strip()
                        modified = True
        
        if modified:
            trip.itinerary = json.loads(json.dumps(itinerary))
            flag_modified(trip, "itinerary")
            updated_trips += 1
            
    if updated_trips > 0:
        db.commit()

    return {
        "success": True,
        "place_name": payload.place_name,
        "image_url": payload.image_url,
        "trips_updated": updated_trips,
        "message": f"Successfully updated image for '{payload.place_name}'"
    }


@router.put("/destinations/image")
def update_destination_image_endpoint(payload: DestinationImageUpdate, db: Session = Depends(get_db)):
    """Allows user to customize/edit the hero image URL for any destination."""
    success = data_service.update_destination_image(
        destination=payload.destination,
        image_url=payload.image_url
    )
    if not success:
        raise HTTPException(status_code=404, detail=f"Destination '{payload.destination}' not found")
    
    return {
        "success": True,
        "destination": payload.destination,
        "image_url": payload.image_url,
        "message": f"Successfully updated hero image for '{payload.destination}'"
    }


@router.post("/upload-image")
def upload_image(payload: ImageUploadPayload, db: Session = Depends(get_db)):
    """
    Accepts a base64 encoded photo from the user's laptop and saves it locally.
    Stores the file in both backend/uploads and frontend/public/uploads,
    and automatically updates places.csv or destinations.csv and database trips.
    """
    if not payload.data_base64:
        raise HTTPException(status_code=400, detail="No image data provided")

    raw_data = payload.data_base64
    # Strip data URL prefix if present (e.g. data:image/jpeg;base64,...)
    if "," in raw_data:
        _, raw_data = raw_data.split(",", 1)

    try:
        image_bytes = base64.b64decode(raw_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Detect extension
    ext = ".jpg"
    orig_name = payload.filename or "photo.jpg"
    if "." in orig_name:
        detected_ext = orig_name.rsplit(".", 1)[1].lower()
        if detected_ext in ["jpg", "jpeg", "png", "webp", "gif", "avif"]:
            ext = f".{detected_ext}"

    # Generate safe unique filename
    label = payload.place_name or payload.destination or "photo"
    clean_label = re.sub(r"[^a-zA-Z0-9_-]", "_", label.strip().lower())[:35]
    timestamp = int(datetime.now().timestamp() * 1000)
    filename = f"{clean_label}_{timestamp}{ext}"

    # Directory targets
    backend_uploads = Path(__file__).resolve().parent.parent.parent / "uploads"
    frontend_uploads = Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "public" / "uploads"

    backend_uploads.mkdir(parents=True, exist_ok=True)
    frontend_uploads.mkdir(parents=True, exist_ok=True)

    backend_file = backend_uploads / filename
    frontend_file = frontend_uploads / filename

    try:
        with open(backend_file, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image to backend storage: {str(e)}")

    try:
        with open(frontend_file, "wb") as f:
            f.write(image_bytes)
    except Exception:
        pass

    public_url = f"/uploads/{filename}"

    # Update places.csv and database trips if for a place
    trips_updated = 0
    if payload.item_type == "place" and payload.place_name:
        data_service.update_place_image(
            place_name=payload.place_name,
            image_url=public_url,
            destination=payload.destination
        )
        trips = db.query(Trip).all()
        for trip in trips:
            itinerary = trip.itinerary
            if not itinerary:
                continue
            modified = False
            if isinstance(itinerary, str):
                try:
                    itinerary = json.loads(itinerary)
                except Exception:
                    continue
            if isinstance(itinerary, dict):
                for day_data in itinerary.values():
                    for place in day_data.get("places", []):
                        if place.get("place_name", "").strip().lower() == payload.place_name.strip().lower():
                            place["image"] = public_url
                            modified = True
            if modified:
                trip.itinerary = json.loads(json.dumps(itinerary))
                flag_modified(trip, "itinerary")
                trips_updated += 1
        if trips_updated > 0:
            db.commit()

    elif payload.item_type == "destination" and payload.destination:
        data_service.update_destination_image(
            destination=payload.destination,
            image_url=public_url
        )

    return {
        "success": True,
        "image_url": public_url,
        "filename": filename,
        "trips_updated": trips_updated,
        "place_name": payload.place_name,
        "destination": payload.destination,
        "message": f"Successfully uploaded photo as {filename}"
    }



# ─── Trip Generation ──────────────────────────────────────────────────────────

@router.post("/trips/generate")
def generate_trip(request: TripGenerateRequest, db: Session = Depends(get_db)):
    """Main ML pipeline endpoint."""
    user_input = request.model_dump()

    result = ml_service.run_ml_pipeline(user_input)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # Save to database
    trip = Trip(
        user_session="demo",
        name=f"Trip to {request.destination}",
        destination=request.destination,
        days=request.days,
        group_size=request.group_size,
        budget=request.budget,
        status="active",
        ml_results=result,
        itinerary=result.get("itinerary", {}),
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {"trip_id": trip.id, **result}


# ─── Trips CRUD ───────────────────────────────────────────────────────────────

@router.get("/trips")
def list_trips(user_session: str = "demo", db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_session == user_session).order_by(Trip.created_at.desc()).all()
    return {"trips": [
        {
            "id": t.id,
            "name": t.name,
            "destination": t.destination,
            "days": t.days,
            "group_size": t.group_size,
            "budget": t.budget,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "total_cost": t.ml_results.get("total_estimated_cost") if t.ml_results else None,
            "traveller_profile": t.ml_results.get("traveller_profile", {}).get("label") if t.ml_results else None,
        }
        for t in trips
    ]}


@router.get("/trips/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {
        "id": trip.id,
        "name": trip.name,
        "destination": trip.destination,
        "days": trip.days,
        "group_size": trip.group_size,
        "budget": trip.budget,
        "status": trip.status,
        "ml_results": trip.ml_results,
        "itinerary": trip.itinerary,
        "created_at": trip.created_at.isoformat() if trip.created_at else None,
    }


@router.put("/trips/{trip_id}")
def update_trip(trip_id: int, update: TripUpdate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if update.name:
        trip.name = update.name
    if update.itinerary is not None:
        trip.itinerary = update.itinerary
        # Recalculate costs from updated itinerary
        if trip.ml_results:
            new_ml = dict(trip.ml_results)
            # Update budget breakdown activities cost
            total_act_cost = sum(
                sum(int(p.get("average_cost", 0)) for p in day.get("places", []))
                for day in update.itinerary.values()
            )
            if "budget_breakdown" in new_ml:
                new_ml["budget_breakdown"]["activities"] = total_act_cost
                base = sum(v for k, v in new_ml["budget_breakdown"].items() if k != "activities" and k != "total")
                new_ml["budget_breakdown"]["total"] = base + total_act_cost
                new_ml["total_estimated_cost"] = new_ml["budget_breakdown"]["total"]
                new_ml["budget_remaining"] = max(0, trip.budget - new_ml["total_estimated_cost"])
            trip.ml_results = new_ml
    if update.status:
        trip.status = update.status
    db.commit()
    db.refresh(trip)
    return {"id": trip.id, "ml_results": trip.ml_results, "itinerary": trip.itinerary}


@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted"}


# ─── Favourites ───────────────────────────────────────────────────────────────

@router.post("/favourites")
def add_favourite(fav: FavouriteCreate, db: Session = Depends(get_db)):
    existing = db.query(Favourite).filter(
        Favourite.user_session == fav.user_session,
        Favourite.item_id == fav.item_id,
    ).first()
    if existing:
        return {"id": existing.id, "message": "Already in favourites"}

    db_fav = Favourite(**fav.model_dump())
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return {"id": db_fav.id, "message": "Added to favourites"}


@router.get("/favourites")
def get_favourites(user_session: str = "demo", db: Session = Depends(get_db)):
    favs = db.query(Favourite).filter(Favourite.user_session == user_session).all()
    return {"favourites": [
        {"id": f.id, "item_type": f.item_type, "item_id": f.item_id,
         "item_name": f.item_name, "item_image": f.item_image,
         "created_at": f.created_at.isoformat() if f.created_at else None}
        for f in favs
    ]}


@router.delete("/favourites/{fav_id}")
def remove_favourite(fav_id: int, db: Session = Depends(get_db)):
    fav = db.query(Favourite).filter(Favourite.id == fav_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favourites"}


# ─── ML Endpoints ─────────────────────────────────────────────────────────────

@router.get("/ml/metrics")
def get_ml_metrics():
    return evaluation.get_all_metrics()


@router.get("/ml/classification")
def get_classification_metrics():
    return evaluation.get_classification_results()


@router.get("/ml/clustering")
def get_clustering_metrics():
    return evaluation.get_clustering_results()


@router.get("/ml/regression")
def get_regression_metrics():
    return evaluation.get_regression_results()


@router.get("/ml/feature-importance")
def get_feature_importance():
    clf_results = evaluation.get_classification_results()
    if "error" in clf_results:
        return clf_results
    return {"feature_importance": clf_results.get("feature_importance", [])}


@router.post("/ml/train")
def train_models(background_tasks: BackgroundTasks):
    """Trigger model training (runs in background)."""
    def do_train():
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from app.ml.train import train_all
        train_all()

    background_tasks.add_task(do_train)
    return {"message": "Model training started in background. Check /api/ml/metrics for status."}


@router.get("/ml/dataset-stats")
def get_dataset_stats():
    return evaluation.get_dataset_stats()
