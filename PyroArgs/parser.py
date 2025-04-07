import inspect
import shlex
from typing import Any, Callable, Dict, List, Tuple, Union

from . import errors


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
    func: Callable, args: str
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

    signature: inspect.Signature = inspect.signature(func)
    lexer: shlex.shlex = shlex.shlex(args.strip(), posix=True)
    lexer.whitespace_split = True
    lexer.escapedquotes = '"'
    lexer.quotes = '"'
    lexer.whitespace = ' \n'
    lexer.commenters = ''
    args_list: List[str] = list(lexer)

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
                arg: str = args_list[args_counter]
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
                        parsed_args=args_list,
                        parsed_kwargs=result_kwargs
                    )

            if not default_used:
                if param.annotation != inspect._empty:
                    try:
                        if param.annotation != Any:
                            arg = param.annotation(arg)
                    except ValueError:
                        raise errors.ArgumentTypeError(
                            name=name,
                            message_object=None,
                            parsed_args=args_list,
                            parsed_kwargs=result_kwargs,
                            errored_arg_name=name,
                            errored_arg_position=args_counter+1,
                            required_type=param.annotation
                        ) from None
                result_args.append(arg)

        elif param.kind == param.KEYWORD_ONLY:
            if is_keyword_only_used:
                raise SyntaxError(
                    'There should not be more than one keyword argument in the function call.'
                )
            is_keyword_only_used = True

            arg = ''
            if args_counter < len(args_list):
                arg: str = (
                    args.split(args_list[args_counter-1], 1)[1]
                    if args_counter > 0
                    else args
                )
            elif args_counter > 0:
                try:
                    parts = args.split(args_list[args_counter - 1], 1)
                    if len(parts) > 1:
                        arg = parts[1].strip()
                except (IndexError, ValueError):
                    pass

            if not arg:
                if param.default != param.empty:
                    arg = param.default

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
                        parsed_args=args_list,
                        parsed_kwargs=result_kwargs,
                        errored_arg_name=name,
                        errored_arg_position=args_counter+1,
                        required_type=param.annotation
                    ) from None
            result_kwargs[name] = arg.strip()

        args_counter += 1

    return result_args, result_kwargs


if __name__ == '__main__':
    def func(message: ..., user: str, ban_time: int = 120, *, reason: str):
        print('---')
        print(user)
        print('---')
        print(ban_time)
        print('---')
        print(reason)
        print('---')

        print(type(user))
        print(type(ban_time))
        print(type(reason))

    args = 'Notch -1 X-Ray'

    result_args, result_kwargs = parse_command(func, args)
    print(result_args, result_kwargs)
    func(..., *result_args, **result_kwargs)
