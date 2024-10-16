from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers.external.otp_service_twilio import send_message_via_twilio, send_whatsapp_message
from db.dbmanager import DBManager

db_manager = DBManager().get_instance()

router = APIRouter()

class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    user_aadhaar_number: str


@router.post("/send_sos")
async def send_sos(request: SOSRequest):
    try:
        # Fetch the nearest 3 police phone numbers based on lat/long
        nearest_police = db_manager.fetch_nearest_police_numbers(
            latitude=request.latitude, 
            longitude=request.longitude
        )
        
        # Fetch the nearest 3 user contact numbers based on lat/long
        nearest_contacts = db_manager.fetch_nearest_phone_numbers(
            latitude=request.latitude, 
            longitude=request.longitude
        )

        # Function to fetch top-priority contact
        def fetch_top_priority_contact(aadhaar_number: str):
            for priority in [3, 2, 1, 0]:
                contact = db_manager.fetch_phone_by_priority(
                    aadhaar_number=aadhaar_number,
                    priority=priority
                )
                if contact:  # If a contact is found for the given priority, return it
                    return contact
            return None  # If no contact is found in any priority

        # Fetch the top priority contact for the user
        top_priority_contact = fetch_top_priority_contact(request.user_aadhaar_number)

        # SOS message text
        sos_message = f"SOS! Emergency at coordinates (Lat: {request.latitude}, Long: {request.longitude}). Please help! Google link: https://maps.google.com/?q={request.latitude},{request.longitude}"

        # Send SOS message to nearest police contacts
        for police in nearest_police['data']:
            send_message_via_twilio(police['phone_number'], sos_message)
            send_whatsapp_message(police['phone_number'], sos_message)
        
        # Send SOS message to nearest user contacts
        for contact in nearest_contacts['data']:
            send_message_via_twilio(contact['phone_number'], sos_message)
            send_whatsapp_message(police['phone_number'], sos_message)

        # Send SOS message to the top priority contact if it exists
        if top_priority_contact:
            send_message_via_twilio(top_priority_contact['phone_number'], sos_message)
            send_whatsapp_message(police['phone_number'], sos_message)

        return JSONResponse(content={"message": "SOS messages sent successfully"}, status_code=200)

    except Exception as e:
        print(f"Error sending SOS: {e}")
        raise HTTPException(status_code=500, detail="Failed to send SOS messages")
