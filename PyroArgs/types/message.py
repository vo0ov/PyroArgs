# PyroArgs/types/message.py
from pyrogram.types import Message as BaseMessage
from typing import Any, Optional


class Message(BaseMessage):
    command_meta_data: Optional[Any] = None
