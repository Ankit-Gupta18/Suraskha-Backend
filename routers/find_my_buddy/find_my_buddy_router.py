from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.dbmanager import DBManager

db_manager = DBManager().get_instance()

router = APIRouter()

# Pydantic model for request
class FindBuddyRequest(BaseModel):
    user_id: int
    source: dict  # Expected format: {"lat": float, "long": float}
    destination: dict  # Expected format: {"lat": float, "long": float}
    date_time: str  # Expected format: "YYYY-MM-DD HH:MM:SS"

# Pydantic model for search
class SearchBuddyRequest(BaseModel):
    source: dict
    destination: dict
    date_time: str
    source_diameter: int
    destination_diameter: int
    time_range: int


@router.post("/add_request")
async def add_request(request: FindBuddyRequest):
    """
    API to add a request to the find_my_buddy table.
    """
    try:
        success = db_manager.insert_find_my_buddy_request(
            user_id=request.user_id,
            source=request.source,
            destination=request.destination,
            date_time=request.date_time
        )

        if success:
            return JSONResponse(content={"message": "Request added successfully"}, status_code=201)
        else:
            raise HTTPException(status_code=500, detail="Failed to add request")

    except Exception as e:
        print(f"Error adding request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/search_request")
async def search_request(request: SearchBuddyRequest):
    """
    API to search for existing requests in the find_my_buddy table.
    """
    try:
        results = db_manager.search_find_my_buddy_requests(
            source=request.source,
            destination=request.destination,
            date_time=request.date_time,
            source_diameter=request.source_diameter,
            destination_diameter=request.destination_diameter,
            time_range=request.time_range
        )

        return JSONResponse(content={"data": results}, status_code=200)

    except Exception as e:
        print(f"Error searching requests: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")