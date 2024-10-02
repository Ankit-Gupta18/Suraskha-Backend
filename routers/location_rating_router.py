from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from db.dbmanager import DBManager
import pandas as pd

db_manager = DBManager().get_instance()

router = APIRouter()


# Model for inserting/updating location rating
class LocationRatingRequest(BaseModel):
    latitude: float
    longitude: float
    location: str
    state: str
    rating: int



# API to fetch location ratings (GET request)
@router.get("/fetch_location_ratings")
async def fetch_location_ratings():
    try:
        ratings_df = db_manager.fetch_location_ratings()

        if ratings_df.empty:
            return {"status": "ok", "message": "No location ratings found."}

        ratings = ratings_df.to_dict(orient="records")
        return {"status": "ok", "ratings": ratings}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch location ratings.")


# API to insert or update location rating (POST request)
@router.post("/insert_or_update_location_rating")
async def insert_or_update_location_rating(payload: LocationRatingRequest):
    try:

        #Insert or update location rating in the database
        updated_location_rating = db_manager.insert_or_update_location_rating(
            location=payload.location,
            state=payload.state,
            latitude=payload.latitude,
            longitude=payload.longitude,
            new_rating=payload.rating
        )

        if updated_location_rating is None:
            raise HTTPException(status_code=500, detail="Failed to insert or update location rating.")

        return {"status": "ok", "message": "Location rating updated.", "data": updated_location_rating.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

