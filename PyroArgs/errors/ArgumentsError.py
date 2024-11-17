# PyroArgs/errors/ArgumentsError.py
from typing import List, Any, Dict
from ..types import Message


class ArgumentsError(Exception):
    def __init__(
        self, name: str,
        message_object: Message,
        parsed_args: List[Any],
        parsed_kwargs: Dict[str, Any],
        error_text: str = ''
    ):
        super().__init__(error_text)
        self.name = name
        self.message_object = message_object
        self.parsed_args = parsed_args
        self.parsed_kwargs = parsed_kwargs
        self.error_text = error_text
