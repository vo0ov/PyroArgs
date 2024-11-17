# tests/test_types/test_events.py
import unittest
from PyroArgs.types.events import Events
from PyroArgs.types.message import Message


class TestEvents(unittest.TestCase):

    def setUp(self):
        self.events = Events()
        self.message = Message()

    def test_on_before_use_command(self):
        called = []

        @self.events.on_before_use_command
        async def handler(message, command, args, kwargs):
            called.append((message, command, args, kwargs))

        self.assertEqual(len(self.events._on_before_use_command_handlers), 1)
        self.assertIs(self.events._on_before_use_command_handlers[0], handler)

    # Similar tests can be written for other event handlers

    def test_trigger_before_use_command(self):
        called = []

        @self.events.on_before_use_command
        async def handler(message, command, args, kwargs):
            called.append((message, command, args, kwargs))

        import asyncio
        asyncio.run(self.events._trigger_before_use_command(
            self.message, 'test', [1], {'a': 2}))
        self.assertEqual(len(called), 1)
        self.assertEqual(called[0], (self.message, 'test', [1], {'a': 2}))


if __name__ == '__main__':
    unittest.main()
