from beanie import Document
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class Conversation(Document):
    messages: List[Message]
    user_id: str

    class Settings:
        collection = "conversations"