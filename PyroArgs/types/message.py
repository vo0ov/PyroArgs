# PyroArgs/types/message.py
from pyrogram.types import Message as BaseMessage
from typing import Any, Optional


class Message(BaseMessage):
    custom_data: Optional[Any] = None
