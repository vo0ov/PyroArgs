# tests/test_errors/test_CommandPermissionError.py
import unittest
from PyroArgs.errors import CommandPermissionError
from PyroArgs.types import Message


class TestCommandPermissionError(unittest.TestCase):

    def test_command_permission_error(self):
        error = CommandPermissionError(
            name='test_command',
            message=Message(),
            permission_level=2
        )
        expected_message = (
            'Permissions error: User does not have permission to use command "test_command".'
        )
        self.assertEqual(error.name, 'test_command')
        self.assertEqual(error.permission_level, 2)
        self.assertEqual(str(error), expected_message)


if __name__ == '__main__':
    unittest.main()
