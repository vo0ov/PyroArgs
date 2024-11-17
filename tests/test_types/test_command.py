# tests/test_types/test_command.py
import unittest
from PyroArgs.types.command import Command


class TestCommand(unittest.TestCase):

    def test_command_creation(self):
        cmd = Command(
            command='start',
            description='Start the bot',
            usage='/start',
            example='/start',
            permissions=0,
            aliases=['run'],
            command_meta_data={'key': 'value'}
        )
        self.assertEqual(cmd.command, 'start')
        self.assertEqual(cmd.description, 'Start the bot')
        self.assertEqual(cmd.usage, '/start')
        self.assertEqual(cmd.example, '/start')
        self.assertEqual(cmd.permissions, 0)
        self.assertEqual(cmd.aliases, ['run'])
        self.assertEqual(cmd.command_meta_data, {'key': 'value'})

    def test_has_permission(self):
        cmd = Command(
            command='admin',
            description='Admin command',
            usage='/admin',
            example='/admin',
            permissions=2
        )
        self.assertTrue(cmd.has_permission(2))
        self.assertTrue(cmd.has_permission(3))
        self.assertFalse(cmd.has_permission(1))


if __name__ == '__main__':
    unittest.main()
