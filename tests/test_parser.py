# tests/test_parser.py
import unittest
from PyroArgs.parser import get_command_and_args, parse_command
from PyroArgs.errors import MissingArgumentError, ArgumentTypeError


class TestParser(unittest.TestCase):

    def test_get_command_and_args(self):
        text = '/start arg1 arg2'
        prefixes = ['/']
        cmd, args = get_command_and_args(text, prefixes)
        self.assertEqual(cmd, 'start')
        self.assertEqual(args, 'arg1 arg2')

    def test_get_command_and_args_no_prefix(self):
        text = 'start arg1 arg2'
        prefixes = ['/']
        with self.assertRaises(NameError):
            get_command_and_args(text, prefixes)

    def test_parse_command_with_correct_args(self):
        def func(a: int, b: str):
            return a, b

        command = '123 hello'
        result_args, result_kwargs = parse_command(func, command)
        self.assertEqual(result_args, [123, 'hello'])
        self.assertEqual(result_kwargs, {})

    def test_parse_command_missing_argument(self):
        def func(a: int, b: str):
            return a, b

        command = '123'
        with self.assertRaises(MissingArgumentError):
            parse_command(func, command)

    def test_parse_command_type_error(self):
        def func(a: int, b: str):
            return a, b

        command = 'hello world'
        with self.assertRaises(ArgumentTypeError):
            parse_command(func, command)

    def test_parse_command_with_default(self):
        def func(a: int, b: str = 'default'):
            return a, b

        command = '123'
        result_args, result_kwargs = parse_command(func, command)
        self.assertEqual(result_args, [123, 'default'])
        self.assertEqual(result_kwargs, {})

    def test_parse_command_keyword_only(self):
        def func(a: int, *, b: str):
            return a, b

        command = '123 hello world'
        result_args, result_kwargs = parse_command(func, command)
        self.assertEqual(result_args, [123])
        self.assertEqual(result_kwargs, {'b': 'hello world'})

    def test_parse_command_var_positional(self):
        def func(a: int, *args):
            return a, args

        command = '123 456 789'
        with self.assertRaises(SyntaxError):
            parse_command(func, command)

    def test_parse_command_var_keyword(self):
        def func(a: int, **kwargs):
            return a, kwargs

        command = '123 key=value'
        with self.assertRaises(SyntaxError):
            parse_command(func, command)

    def test_parse_command_bool(self):
        def func(a: bool):
            return a

        command_true = 'true'
        command_false = 'false'
        result_args_true, _ = parse_command(func, command_true)
        result_args_false, _ = parse_command(func, command_false)
        self.assertTrue(result_args_true[0])
        self.assertFalse(result_args_false[0])

    def test_get_bool_invalid_value(self):
        def func(a: bool):
            return a

        command = 'maybe'
        with self.assertRaises(ValueError):
            parse_command(func, command)


if __name__ == '__main__':
    unittest.main()
