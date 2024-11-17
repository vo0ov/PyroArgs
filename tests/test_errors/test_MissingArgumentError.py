# tests/test_errors/test_MissingArgumentError.py
import unittest
from PyroArgs.errors import MissingArgumentError
from PyroArgs.types import Message


class TestMissingArgumentError(unittest.TestCase):

    def test_missing_argument_error(self):
        error = MissingArgumentError(
            name='test_command',
            message_object=Message(),
            parsed_args=[1],
            parsed_kwargs={},
            missing_arg_name='arg2',
            missing_arg_position=2
        )
        expected_message = (
            'MissingArgumentError: Missing required argument "arg2" at position 2.'
        )
        self.assertEqual(error.name, 'test_command')
        self.assertEqual(error.missing_arg_name, 'arg2')
        self.assertEqual(error.missing_arg_position, 2)
        self.assertEqual(str(error), expected_message)


if __name__ == '__main__':
    unittest.main()
