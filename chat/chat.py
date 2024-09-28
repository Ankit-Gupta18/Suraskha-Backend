from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .websocket_manager import ConnectionManager
from .db_manager_chats import DBManager
import json
from datetime import datetime

router = APIRouter()

manager = ConnectionManager()
db_manager = DBManager.get_instance()

@router.websocket("/ws/chat/{sender_id}/{receiver_id}")
async def chat_websocket(websocket: WebSocket, sender_id: int, receiver_id: int):
    await manager.connect(sender_id, websocket)
    try:
        # Optionally, send chat history upon connection
        chat_history = await db_manager.get_chat_history(sender_id, receiver_id)
        if chat_history:
            # Debug: Print each message's timestamp and type
            history_messages = [
                {
                    "sender_id": msg[0],  # sender_id from the database
                    "message": msg[1],
                    "timestamp": msg[2].isoformat() if isinstance(msg[2], datetime) else msg[2]
                }
                for msg in chat_history
            ]
            await websocket.send_text(json.dumps({"history": history_messages}))

        while True:
            data = await websocket.receive_text()
            # Save message to the database
            await db_manager.save_message(sender_id, receiver_id, data)
            # Send message to receiver if they are connected
            await manager.send_personal_message(
                json.dumps({
                    "sender_id": sender_id,
                    "message": data,
                    "timestamp": datetime.utcnow().isoformat()
                }),
                receiver_id
            )
    except WebSocketDisconnect:
        print(f"User {sender_id} disconnected.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(sender_id)
