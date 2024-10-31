# tests/test_pyroargs.py
import aiounittest
from PyroArgs import PyroArgs, types
from pyrogram import Client
from unittest.mock import MagicMock


class TestPyroArgs(aiounittest.AsyncTestCase):
    def setUp(self):
        self.bot = MagicMock(spec=Client)
        self.pyro_args = PyroArgs(self.bot, prefixes=["/"])

    # Другие тесты остаются без изменений

    async def test_command_custom_data(self):
        custom_data = {"key": "value"}

        @self.pyro_args.command(custom_data=custom_data)
        async def test_cmd(message: types.Message):
            pass  # Здесь нет возврата значения

        message = MagicMock(spec=types.Message)
        message.text = "/test_cmd"
        message.custom_data = None

        client = self.bot
        await test_cmd._pyroargs_handler(client, message)

        self.assertEqual(message.custom_data, custom_data)
