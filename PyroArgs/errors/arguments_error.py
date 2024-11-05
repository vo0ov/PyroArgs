# PyroArgs/errors/arguments_error.py
from typing import List, Any, Dict
from ..types import Message


class ArgumentsError(Exception):
    def __init__(
        self, command: str,  # REQUIRED FOR ALL ERRORS
        message: Message,  # REQUIRED FOR ALL ERRORS
        parsed_args: List[Any],  # REQUIRED FOR ALL ERRORS
        parsed_kwargs: Dict[str, Any],  # REQUIRED FOR ALL ERRORS
        missing_arg: str,
        arg_position: int
    ):
        full_message = (
            f'ArgumentsError: Missing required argument "{missing_arg}" at position {arg_position} in command "{command}". '
            f'Current args: {parsed_args}, kwargs: {parsed_kwargs}'
        )
        super().__init__(full_message)
        self.command = command
        self.message = message
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
        self.missing_arg = missing_arg
        self.arg_position = arg_position
