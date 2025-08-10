from pyrogram.types import Message


class CommandPermissionError(Exception):
    def __init__(
        self,
        command: str,
        message: Message,
        permission_level: int
    ) -> None:
        full_message = ('Permissions error: User does not '
                        f'have permission to use command "{command}".')
        super().__init__(full_message)
        self.command = command
        self.message = message
        self.permission_level = permission_level
