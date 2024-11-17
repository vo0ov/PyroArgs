# PyroArgs/errors/MissingArgumentError.py
from .ArgumentsError import ArgumentsError
from ..types import Message
from typing import List, Any, Dict


class MissingArgumentError(ArgumentsError):
    def __init__(
        self,
        name: str,
        message_object: Message,
        parsed_args: List[Any],
        parsed_kwargs: Dict[str, Any],
        missing_arg_name: str,
        missing_arg_position: int
    ):
        full_message = (
            f'MissingArgumentError: Missing required argument "{missing_arg_name}" at position {missing_arg_position}.'
        )

        super().__init__(name, message_object, parsed_args,
                         parsed_kwargs, full_message)

        self.missing_arg_name = missing_arg_name
        self.missing_arg_position = missing_arg_position
