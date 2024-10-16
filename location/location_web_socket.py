# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from chat.websocket_manager import ConnectionManager
import json
from db.dbmanager import DBManager

db_manager = DBManager().get_instance()

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            location = json.loads(data)
            print(f"Received location from user {user_id}: {location}")

            nearest_police = db_manager.fetch_nearest_police_numbers(
                latitude=location.latitude, 
                longitude=location.longitude
            )
            nearest_contacts = db_manager.fetch_nearest_phone_numbers(
                latitude=location.latitude, 
                longitude=location.longitude
            )

            # Store or update location in the database
            db_manager.update_user_location(location.latitude, location.longitude)

            # Send other users' locations to the current user
            message_data = {
                "nearest_user_contacts_location": nearest_contacts,
                "nearest_police_location": nearest_police
            }

            # Send the combined data as a JSON string
            await manager.send_personal_message(json.dumps(message_data), user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
