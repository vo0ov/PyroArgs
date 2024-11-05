# PyroArgs/types/events.py
from typing import List, Callable, Dict, Any

from . import Message
from .logger import Logger
from ..errors import ArgumentsError, CommandError, PermissionsError


class Events:
    def __init__(self) -> None:
        self._on_use_command_handlers: List[Callable[[
            str, str, List[Any], Dict[str, Any]], Any]] = []
        self._on_arguments_error_handlers: List[Callable[[
            Message, ArgumentsError], Any]] = []
        self._on_command_error_handlers: List[Callable[[
            Message, CommandError], Any]] = []
        self._on_permissions_error_handlers: List[Callable[[
            Message, PermissionsError], Any]] = []
        self.logger: Logger = Logger()

    # * DECORATORS * #
    def on_use_command(
        self,
        func: Callable[[str, str, List[Any], Dict[str, Any]], Any]
    ) -> Callable[[str, str, List[Any], Dict[str, Any]], Any]:
        """Декоратор для регистрации обработчиков успешного использования команды."""
        self._on_use_command_handlers.append(func)
        return func

    def on_arguments_error(self, func: Callable[[Message, ArgumentsError], Any]) -> Callable[[Message, ArgumentsError], Any]:
        """Декоратор для регистрации обработчиков ошибок аргументов."""
        self._on_arguments_error_handlers.append(func)
        return func

    def on_command_error(self, func: Callable[[Message, CommandError], Any]) -> Callable[[Message, CommandError], Any]:
        """Декоратор для регистрации обработчиков ошибок команд."""
        self._on_command_error_handlers.append(func)
        return func

    def on_permissions_error(
        self, func: Callable[[Message, PermissionsError], Any]
    ) -> Callable[[Message, PermissionsError], Any]:
        """Декоратор для регистрации обработчиков ошибок команд."""
        self._on_permissions_error_handlers.append(func)
        return func

    # * TRIGGERS METHODS * #
    async def _trigger_use_command(
        self, message: Message, command: str, parsed_args: List[Any], parsed_kwargs: Dict[str, Any]
    ) -> None:
        """Вызов всех зарегистрированных обработчиков успешного использования команды."""
        await self.logger.trigger_use_command(
            message, command, parsed_args, parsed_kwargs)

        for handler in self._on_use_command_handlers:
            await handler(message, command, parsed_args, parsed_kwargs)

    async def _trigger_arguments_error(self, message: Message, error: ArgumentsError) -> None:
        """Вызов всех зарегистрированных обработчиков ошибок аргументов."""
        await self.logger.trigger_arguments_error(error)

        for handler in self._on_arguments_error_handlers:
            await handler(message, error)

    async def _trigger_command_error(self, message: Message, error: CommandError) -> None:
        """Вызов всех зарегистрированных обработчиков ошибок команд."""
        await self.logger.trigger_command_error(error)

        for handler in self._on_command_error_handlers:
            await handler(message, error)

    async def _trigger_permissions_error(self, message: Message, error: PermissionsError) -> None:
        """Вызов всех зарегистрированных обработчиков ошибок команд."""
        await self.logger.trigger_permissions_error(error)

        for handler in self._on_permissions_error_handlers:
            await handler(message, error)
