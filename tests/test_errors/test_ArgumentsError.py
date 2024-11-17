# tests/test_errors/test_ArgumentsError.py
import unittest
from PyroArgs.errors import ArgumentsError
from PyroArgs.types import Message


class TestArgumentsError(unittest.TestCase):

    def test_arguments_error(self):
        error = ArgumentsError(
            name='test_command',
            message_object=Message(),
            parsed_args=[1, 2],
            parsed_kwargs={'a': 3},
            error_text='An error occurred.'
        )
        self.assertEqual(error.name, 'test_command')
        self.assertEqual(error.parsed_args, [1, 2])
        self.assertEqual(error.parsed_kwargs, {'a': 3})
        self.assertEqual(str(error), 'An error occurred.')


if __name__ == '__main__':
    unittest.main()
