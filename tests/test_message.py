# tests/test_message.py
import unittest
from PyroArgs.types import Message
from pyrogram.types import Message as BaseMessage
from pyrogram.types import Chat, User


class TestMessage(unittest.TestCase):
    def test_message_inheritance(self):
        message = Message(
            id=1,
            chat=Chat(id=12345, type="private"),
            date=0,
            from_user=User(id=67890, is_bot=False, first_name="TestUser")
        )
        self.assertIsInstance(message, BaseMessage)

    def test_custom_data(self):
        message = Message(
            id=1,
            chat=Chat(id=12345, type="private"),
            date=0,
            from_user=User(id=67890, is_bot=False, first_name="TestUser")
        )
        self.assertIsNone(message.custom_data)
        message.custom_data = "Test Data"
        self.assertEqual(message.custom_data, "Test Data")
