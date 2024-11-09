# PyroArgs/errors/command_error.py
from typing import List, Dict, Any
from ..types import Message


class CommandError(Exception):
    def __init__(
        self,
        command: str,  # REQUIRED FOR ALL ERRORS
        message: Message,  # REQUIRED FOR ALL ERRORS
        parsed_args: List[Any],  # REQUIRED FOR ALL ERRORS
        parsed_kwargs: Dict[str, Any],  # REQUIRED FOR ALL ERRORS
        error_message: str = None,
        original_error: Exception = None
    ):
        full_message = f'Command error: Error in command "{command}".'
        super().__init__(full_message)
        self.command = command
        self.message = message
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
        self.error_message = error_message
        self.original_error = original_error
