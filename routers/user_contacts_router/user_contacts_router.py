from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.dbmanager import DBManager

# Instantiate the DB Manager
db_manager = DBManager().get_instance()

# Define the API router
router = APIRouter()

# Request payload model for adding or updating user contact
class UserContactRequest(BaseModel):
    aadhaar_number: int
    name: str
    relation: str
    phone_number: str
    email: str
    status: str
    priority: int  # Priority (0-5)
    latitude: float  # Decimal places limited to 3 in database
    longitude: float  # Decimal places limited to 3 in database

# Request payload model for deleting a user contact by phone number
class DeleteUserContactRequest(BaseModel):
    phone_number: str

# Request payload model for updating user contact (including old phone number)
class UpdateUserContactRequest(BaseModel):
    phone_number: str
    aadhaar_number: int
    name: str
    relation: str
    new_phone_number: str  # New phone number
    email: str
    status: str
    priority: int  # Priority (0-5)
    latitude: float  # Decimal places limited to 3 in database
    longitude: float  # Decimal places limited to 3 in database

# API Endpoint for adding a user contact
@router.post("/add_user_contact")
async def add_user_contact(payload: UserContactRequest):
    # Ensure valid priority range
    if not (0 <= payload.priority <= 5):
        raise HTTPException(status_code=400, detail="Priority must be between 0 and 5.")

    # Prepare the payload dictionary
    contact_payload = {
        "aadhaar_number": payload.aadhaar_number,
        "name": payload.name,
        "relation": payload.relation,
        "phone_number": payload.phone_number,
        "email": payload.email,
        "status": payload.status,
        "priority": payload.priority,
        "latitude": payload.latitude,
        "longitude": payload.longitude
    }

    # Insert the user contact into the database
    result = db_manager.insert_user_contact(contact_payload)

    # Handle the result of the insert operation
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {"status": "ok", "message": result["message"]}

# API Endpoint for deleting a user contact by phone number
@router.delete("/delete_user_contact")
async def delete_user_contact(payload: DeleteUserContactRequest):
    # Prepare the phone number
    phone_number = payload.phone_number

    # Delete the user contact from the database
    result = db_manager.delete_user_contact_by_phone(phone_number)

    # Handle the result of the delete operation
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {"status": "ok", "message": result["message"]}

# API Endpoint for updating a user contact
@router.put("/update_user_contact")
async def update_user_contact(payload: UpdateUserContactRequest):
    # Ensure valid priority range
    if not (0 <= payload.priority <= 5):
        raise HTTPException(status_code=400, detail="Priority must be between 0 and 5.")

    # Prepare the payload dictionary
    contact_payload = {
        "aadhaar_number": payload.aadhaar_number,
        "name": payload.name,
        "relation": payload.relation,
        "new_phone_number": payload.new_phone_number,  # New phone number
        "email": payload.email,
        "status": payload.status,
        "priority": payload.priority,
        "latitude": payload.latitude,
        "longitude": payload.longitude
    }

    # Update the user contact in the database based on the old phone number
    result = db_manager.update_user_contact_by_phone(payload.phone_number, contact_payload)

    # Handle the result of the update operation
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {"status": "ok", "message": result["message"]}
