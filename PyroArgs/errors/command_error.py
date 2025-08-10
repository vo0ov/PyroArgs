from typing import Any, Dict, List

from pyrogram.types import Message


class CommandError(Exception):
    def __init__(
        self,
        command: str,
        message: Message,
        parsed_args: List[Any],
        parsed_kwargs: Dict[str, Any],
        error_message: str = None,
        original_error: Exception = None
    ) -> None:
        full_message = f'Command error: Error in command "{command}".'
        super().__init__(full_message)
        self.command = command
        self.message = message
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
        self.error_message = error_message
        self.original_error = original_error
