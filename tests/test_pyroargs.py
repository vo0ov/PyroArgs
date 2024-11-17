# tests/test_pyroargs.py
import unittest
from pyrogram import Client
from PyroArgs.pyroargs import PyroArgs
from PyroArgs.types.message import Message
from PyroArgs.errors import CommandPermissionError
from unittest.mock import MagicMock


class TestPyroArgs(unittest.TestCase):

    def setUp(self):
        self.client = Client('test_bot')
        self.pyroargs = PyroArgs(self.client)

    def test_command_decorator(self):
        @self.pyroargs.command(name='test')
        async def test_command(message, arg1):
            return arg1

        self.assertIn(
            'test', self.pyroargs.registry.commands['General'][0].command)

    def test_permission_checker(self):
        called = []

        @self.pyroargs.permissions_checker
        async def checker(message, level):
            called.append((message, level))
            return False

        @self.pyroargs.command(name='admin', permissions_level=2)
        async def admin_command(message):
            pass

        message = Message()
        message.text = '/admin'
        message.from_user = MagicMock(id=123)

        handler = self.pyroargs.bot.handlers[0][0].callback

        with self.assertRaises(CommandPermissionError):
            import asyncio
            asyncio.run(handler(self.client, message))

        self.assertEqual(len(called), 1)
        self.assertEqual(called[0][1], 2)


if __name__ == '__main__':
    unittest.main()
