# modals/messageModel.py
from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    content: str
    timestamp: datetime
