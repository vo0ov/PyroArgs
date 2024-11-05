# PyroArgs/errors/command_error.py
from typing import List, Dict, Any
from ..types import Message


class PermissionsError(Exception):
    def __init__(
        self,
        command: str,  # REQUIRED FOR ALL ERRORS
        message: Message,  # REQUIRED FOR ALL ERRORS
        parsed_args: List[Any],  # REQUIRED FOR ALL ERRORS
        parsed_kwargs: Dict[str, Any]  # REQUIRED FOR ALL ERRORS
    ):
        full_message = f'Permissions error: User does not have permission to use command "{command}".'
        super().__init__(full_message)
        self.command = command
        self.message = message
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
