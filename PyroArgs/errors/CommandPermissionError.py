# PyroArgs/errors/PermissionsError.py
from ..types import Message


class CommandPermissionError(Exception):
    def __init__(
        self,
        name: str,
        message: Message,
        permission_level: int
    ):
        full_message = f'Permissions error: User does not have permission to use command "{name}".'
        super().__init__(full_message)
        self.name = name
        self.message = message
        self.permission_level = permission_level
