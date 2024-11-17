# PyroArgs/errors/CommandError.py
from typing import List, Dict, Any
from ..types import Message


class CommandError(Exception):
    def __init__(
        self,
        name: str,
        message: Message,
        parsed_args: List[Any],
        parsed_kwargs: Dict[str, Any],
        error_message: str = None,
        original_error: Exception = None
    ):
        full_message = f'Command error: Error in command "{name}".'
        super().__init__(full_message)
        self.name = name
        self.message = message
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
        self.error_message = error_message
        self.original_error = original_error
