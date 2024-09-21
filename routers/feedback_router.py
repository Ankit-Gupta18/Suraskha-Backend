from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.dbmanager import DBManager

db_manager = DBManager().get_instance()

# Define the API router
router = APIRouter()

# Request payload model for Feedback
class FeedbackRequest(BaseModel):
    name: str
    email: str
    feedback: str
    stars: int 

# API Endpoint for submitting feedback
@router.post("/feedback")
async def submit_feedback(payload: FeedbackRequest):
    # Ensure valid rating range
    if not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    # Prepare the payload dictionary
    feedback_payload = {
        "name": payload.name,
        "email": payload.email,
        "feedback": payload.feedback,
        "stars": payload.stars
    }

    # Insert the feedback into the database
    result = db_manager.insert_feedback(feedback_payload)

    # Handle the result of the insert operation
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {"status": "ok", "message": result["message"]}
