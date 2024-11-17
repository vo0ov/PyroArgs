# tests/test_errors/test_ArgumentTypeError.py
import unittest
from PyroArgs.errors import ArgumentTypeError
from PyroArgs.types import Message


class TestArgumentTypeError(unittest.TestCase):

    def test_argument_type_error(self):
        error = ArgumentTypeError(
            name='test_command',
            message_object=Message(),
            parsed_args=['abc'],
            parsed_kwargs={},
            errored_arg_name='arg1',
            errored_arg_position=1,
            required_type=int
        )
        expected_message = (
            'ArgumentTypeError: Argument "arg1" at position 1 cannot convert to required type "int".'
        )
        self.assertEqual(error.name, 'test_command')
        self.assertEqual(error.errored_arg_name, 'arg1')
        self.assertEqual(error.errored_arg_position, 1)
        self.assertEqual(error.required_type, int)
        self.assertEqual(str(error), expected_message)


if __name__ == '__main__':
    unittest.main()
