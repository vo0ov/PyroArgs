from typing import List, Optional


class Command:
    def __init__(
        self,
        command: str,
        description: str,
        usage: str,
        example: str,
        permissions: int = 0,
        aliases: Optional[List[str]] = None
    ) -> None:
        self.command = command
        self.description = description
        self.usage = usage
        self.example = example
        self.permissions = permissions
        self.aliases = aliases or []

    def has_permission(self, user_level: int) -> bool:
        """Проверяет, имеет ли пользователь необходимый уровень доступа."""
        return user_level >= self.permissions
