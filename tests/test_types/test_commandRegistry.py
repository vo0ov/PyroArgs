# tests/test_types/test_commandRegistry.py
import unittest
from PyroArgs.types.commandRegistry import CommandRegistry
from PyroArgs.types.command import Command


class TestCommandRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = CommandRegistry()
        self.command1 = Command(
            command='start',
            description='Start the bot',
            usage='/start',
            example='/start',
            permissions=0
        )
        self.command2 = Command(
            command='help',
            description='Help command',
            usage='/help',
            example='/help',
            permissions=0,
            aliases=['h']
        )
        self.registry.add_command(self.command1, 'General')
        self.registry.add_command(self.command2, 'General')

    def test_add_command(self):
        self.assertIn('General', self.registry.commands)
        self.assertEqual(len(self.registry.commands['General']), 2)

    def test_get_commands_by_category(self):
        cmds = self.registry.get_commands_by_category('General')
        self.assertEqual(cmds, [self.command1, self.command2])

    def test_find_command(self):
        cmd = self.registry.find_command('start')
        self.assertEqual(cmd, self.command1)
        cmd_alias = self.registry.find_command('h')
        self.assertEqual(cmd_alias, self.command2)
        cmd_none = self.registry.find_command('nonexistent')
        self.assertIsNone(cmd_none)

    def test_iterate_categories(self):
        categories = list(self.registry.iterate_categories())
        self.assertEqual(categories, ['General'])

    def test_iterate_commands(self):
        cmds = list(self.registry.iterate_commands())
        self.assertEqual(cmds, [self.command1, self.command2])

    def test_iterate_categories_with_commands(self):
        categories_with_cmds = list(
            self.registry.iterate_categories_with_commands())
        self.assertEqual(categories_with_cmds, [
                         ('General', [self.command1, self.command2])])


if __name__ == '__main__':
    unittest.main()
