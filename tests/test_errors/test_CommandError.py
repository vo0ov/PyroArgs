# tests/test_errors/test_CommandError.py
import unittest
from PyroArgs.errors import CommandError
from PyroArgs.types import Message


class TestCommandError(unittest.TestCase):

    def test_command_error(self):
        original_exception = ValueError('Invalid value')
        error = CommandError(
            name='test_command',
            message=Message(),
            parsed_args=[1, 2],
            parsed_kwargs={'a': 3},
            error_message='An error occurred.',
            original_error=original_exception
        )
        expected_message = 'Command error: Error in command "test_command".'
        self.assertEqual(error.name, 'test_command')
        self.assertEqual(error.error_message, 'An error occurred.')
        self.assertEqual(error.original_error, original_exception)
        self.assertEqual(str(error), expected_message)


if __name__ == '__main__':
    unittest.main()
