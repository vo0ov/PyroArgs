# PyroArgs/types/command.py
from typing import Optional, List, Any


class Command:
    def __init__(
        self,
        command: str,
        description: str,
        usage: str,
        example: str,
        permissions: int = 0,
        aliases: Optional[List[str]] = None,
        command_meta_data: Any = None
    ):
        self.command = command
        self.description = description
        self.usage = usage
        self.example = example
        self.permissions = permissions
        self.command_meta_data = command_meta_data
        self.aliases = aliases or []

    def has_permission(self, user_level: int) -> bool:
        """Проверяет, имеет ли пользователь необходимый уровень доступа."""
        return user_level >= self.permissions
