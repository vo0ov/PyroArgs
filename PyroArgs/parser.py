from typing import Dict, Any, List, Callable, Union, Tuple
from . import errors
import inspect
import shlex


def get_command_and_args(text: str, prefixes: Union[List[str], Tuple[str], str]) -> Tuple[str, str]:
    """
    Gets command and arguments from a string.

    The function takes a string and a list/tuple of prefixes as parameters.
    It first strips the string of any whitespaces, then checks if the string
    starts with any of the prefixes. If not, it raises a NameError.

    Then it splits the string by spaces and takes the first part as the command.
    It goes through the list of prefixes and checks if the command starts with
    any of them. If it does, it removes the prefix from the command.

    Finally, it takes the rest of the string as the arguments, strips it of any
    whitespaces and returns a tuple with the command and arguments.

    Parameters
    ----------
    text : str
        The string to parse.
    prefixes : List[str] or Tuple[str] or str
        The list/tuple or single prefix to check against.

    Returns
    -------
    Tuple[str, str]
        The command and arguments as a tuple.
    """
    text = text.strip()

    if not text.startswith(tuple(prefixes)):
        raise NameError('Command does not start with prefix.')

    cmd = text.split()[0]
    for prefix in prefixes:
        if cmd.startswith(prefix):
            cmd = cmd[len(prefix):]
            break

    args = text[len(prefix)+len(cmd):].strip()
    return cmd, args


def parse_command(
    func: Callable, command: str, trues: Union[List[str], Tuple[str], str] = ('true', 'yes'),
    falses: Union[List[str], Tuple[str], str] = ('false', 'no')
) -> Any:
    """
    Executes the given function `func` with arguments parsed from the `command` string.

    Args:
        func (Callable): The function to be executed.
        command (str): The command string containing arguments for the function.
        trues (Union[List[str], Tuple[str], str], optional): A list or tuple of strings to interpret as True.
        falses (Union[List[str], Tuple[str], str], optional): A list or tuple of strings to interpret as False.

    Returns:
        Any: The result of executing `func` with the parsed arguments.

    Raises:
        ValueError: If a parameter is missing, casting fails, or multiple keyword-only arguments are used.
    """
    def get_bool(arg: str, trues: Union[List[str], Tuple[str], str] = ('true', 'yes'),
                 falses: Union[List[str], Tuple[str], str] = ('false', 'no')) -> bool:
        """
        Converts a string argument to a boolean.

        Args:
            arg (str): The argument to be converted.
            trues (Union[List[str], Tuple[str], str], optional): A list or tuple of strings to interpret as True.
            falses (Union[List[str], Tuple[str], str], optional): A list or tuple of strings to interpret as False.

        Returns:
            bool: The converted boolean value.

        Raises:
            ValueError: If the argument is not in the trues or falses lists.
        """
        if isinstance(trues, str):
            trues = [trues]
        if isinstance(falses, str):
            falses = [falses]
        if arg.lower() in trues:
            return True
        if arg.lower() in falses:
            return False
        raise ValueError(
            f'Failed to cast argument "{arg}" to bool.')

    signature: inspect.Signature = inspect.signature(func)
    lexer: shlex.shlex = shlex.shlex(command.strip(), posix=True)
    lexer.whitespace_split = True
    lexer.escapedquotes = '"'
    lexer.quotes = '"'
    lexer.whitespace = ' '
    args: List[str] = list(lexer)

    args_counter: int = 0
    result_args: List[Any] = []
    result_kwargs: Dict[str, Any] = {}
    is_keyword_only_used: bool = False

    for param in signature.parameters.values():
        if param.kind == param.VAR_POSITIONAL:
            raise SyntaxError(
                f'Positional var are not supported. Remove "*{param.name}".'
            )
        elif param.kind == param.VAR_KEYWORD:
            raise SyntaxError(
                f'Keyword var are not supported. Remove "**{param.name}".'
            )

    for name, param in list(signature.parameters.items())[1:]:
        # HINT: print(name, param.kind, param.default, param.annotation)
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            default_used: bool = False
            try:
                arg: str = args[args_counter]
            except IndexError:
                if param.default != param.empty:
                    default_used = True
                    arg = param.default
                    result_args.append(arg)
                else:
                    raise errors.MissingArgumentError(
                        name=name,
                        message_object=None,
                        missing_arg_name=name,
                        missing_arg_position=args_counter+1,
                        parsed_args=args,
                        parsed_kwargs=result_kwargs
                    )

            if not default_used:
                if param.annotation == bool:
                    arg = get_bool(arg, trues, falses)

                elif param.annotation != inspect._empty:
                    try:
                        if param.annotation != Any:
                            arg = param.annotation(arg)
                    except ValueError:
                        raise errors.ArgumentTypeError(
                            name=name,
                            message_object=None,
                            parsed_args=args,
                            parsed_kwargs=result_kwargs,
                            errored_arg_name=name,
                            errored_arg_position=args_counter+1,
                            required_type=param.annotation
                        )
                result_args.append(arg)

        elif param.kind == param.KEYWORD_ONLY:
            if is_keyword_only_used:
                raise SyntaxError(
                    'There should not be more than one keyword argument in the function call.'
                )
            is_keyword_only_used = True

            arg: str = ' '.join(args[args_counter:])
            if not arg:
                if param.default != param.empty:
                    arg = param.default

            if param.annotation == bool:
                arg = get_bool(arg, trues, falses)

            elif param.annotation != inspect._empty:
                try:
                    if param.annotation != Any:
                        if arg == '':
                            arg = param.annotation()
                        else:
                            arg = param.annotation(arg)
                except ValueError:
                    raise errors.ArgumentTypeError(
                        name=name,
                        message_object=None,
                        parsed_args=args,
                        parsed_kwargs=result_kwargs,
                        errored_arg_name=name,
                        errored_arg_position=args_counter+1,
                        required_type=param.annotation
                    )
            result_kwargs[name] = arg

        args_counter += 1

    # return func(*result_args, **result_kwargs)
    return result_args, result_kwargs


if __name__ == '__main__':
    def func(a: str, b: bool = '52') -> None:
        print(a, b, sep='\n')
        print(type(a), type(b), sep='\n')
        return 'RESULT_AR'

    text = '/test 111 true'
    cmd, args = get_command_and_args(text, ['/', 'v?'])

    if cmd == 'test':
        result_args, result_kwargs = parse_command(func, args)
        print(func(*result_args, **result_kwargs))
