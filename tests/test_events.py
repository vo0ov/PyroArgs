# tests/test_events.py
import aiounittest
from PyroArgs import PyroArgs, types, errors
from pyrogram import Client
from unittest.mock import MagicMock


class TestEvents(aiounittest.AsyncTestCase):

    def setUp(self):
        self.bot = MagicMock(spec=Client)
        self.pyro_args = PyroArgs(self.bot, prefixes=["/"])

    async def test_arguments_error_event(self):
        handler_called = False

        async def arguments_error_handler(message: types.Message, error: errors.ArgumentsError):
            nonlocal handler_called
            handler_called = True

        self.pyro_args.events.on_arguments_error(arguments_error_handler)

        @self.pyro_args.command()
        async def test_cmd(message: types.Message, arg1: str):
            pass

        message = MagicMock(spec=types.Message)
        message.text = "/test_cmd"
        message.custom_data = None

        client = self.bot
        await test_cmd._pyroargs_handler(client, message)

        self.assertTrue(handler_called)

    async def test_command_error_event(self):
        handler_called = False

        async def command_error_handler(message: types.Message, error: errors.CommandError):
            nonlocal handler_called
            handler_called = True

        self.pyro_args.events.on_command_error(command_error_handler)

        @self.pyro_args.command()
        async def test_cmd(message: types.Message):
            raise Exception("Test exception")

        message = MagicMock(spec=types.Message)
        message.text = "/test_cmd"
        message.custom_data = None

        client = self.bot
        await test_cmd._pyroargs_handler(client, message)

        self.assertTrue(handler_called)
