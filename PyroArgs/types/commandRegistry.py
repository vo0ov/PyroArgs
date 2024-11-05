# PyroArgs/types/commandRegistry.py
from typing import Dict, List, Optional, Iterator, Tuple
from .command import Command


class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, List[Command]] = {}

    def add_command(self, command: Command, category: str):
        """Добавляет новую команду в указанную категорию."""
        if category not in self.commands:
            self.commands[category] = []
        self.commands[category].append(command)

    def get_commands_by_category(self, category: str) -> List[Command]:
        """Возвращает список команд по категории."""
        return self.commands.get(category, [])

    def find_command(self, command_name: str) -> Optional[Command]:
        """Ищет команду по её названию или алиасу."""
        for cmds in self.commands.values():
            for cmd in cmds:
                if cmd.command == command_name or command_name in cmd.aliases:
                    return cmd
        return None

    def iterate_categories(self) -> Iterator[str]:
        """Итерация по всем категориям."""
        for category in self.commands:
            yield category

    def iterate_commands(self) -> Iterator[Command]:
        """Итерация по всем командам."""
        for cmds in self.commands.values():
            for cmd in cmds:
                yield cmd

    def iterate_categories_with_commands(self) -> Iterator[Tuple[str, List[Command]]]:
        """Итерация по всем категориям и командам."""
        for category in self.commands:
            yield category, self.commands[category]
