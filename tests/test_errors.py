# tests/test_errors.py
import unittest
from PyroArgs import errors


class TestErrors(unittest.TestCase):
    def test_arguments_error(self):
        try:
            raise errors.ArgumentsError("Test ArgumentsError")
        except errors.ArgumentsError as e:
            self.assertEqual(str(e), "Test ArgumentsError")
            self.assertEqual(e.__module__, 'PyroArgs.errors')

    def test_command_error(self):
        try:
            raise errors.CommandError("Test CommandError")
        except errors.CommandError as e:
            self.assertEqual(str(e), "Test CommandError")
            self.assertEqual(e.__module__, 'PyroArgs.errors')
