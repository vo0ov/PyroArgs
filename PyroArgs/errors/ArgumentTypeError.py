# PyroArgs/errors/ArgumentTypeError.py
from .ArgumentsError import ArgumentsError
from typing import List, Any, Dict
from ..types import Message


class ArgumentTypeError(ArgumentsError):
    def __init__(
        self,
        name: str,
        message_object: Message,
        parsed_args: List[Any],
        parsed_kwargs: Dict[str, Any],
        errored_arg_name: str,
        errored_arg_position: int,
        required_type: type
    ):
        full_message = (
            f'ArgumentTypeError: Argument "{errored_arg_name}" at position '
            f'{errored_arg_position} cannot convert to required type '
            f'"{required_type}".'
        )

        super().__init__(name, message_object, parsed_args,
                         parsed_kwargs, full_message)

        self.errored_arg_name = errored_arg_name
        self.errored_arg_position = errored_arg_position
        self.required_type = required_type
