# PyroArgs/types/events.py
from typing import List, Callable, Dict, Any, TypeAlias

from .logger import Logger
from . import Message
from .. import errors


CommandHandler: TypeAlias = Callable[[
    str, str, List[Any], Dict[str, Any]], Any]

ErrorHandler: TypeAlias = Callable[[Message, errors.ArgumentsError], Any]

CommandErrorHandler: TypeAlias = Callable[[Message, errors.CommandError], Any]

PermissionErrorHandler: TypeAlias = Callable[[
    Message, errors.CommandPermissionError], Any]


class Events:
    def __init__(self, log_file: str = None) -> None:
        self._on_before_use_command_handlers: List[CommandHandler] = []
        self._on_after_use_command_handlers: List[CommandHandler] = []
        self._on_missing_argument_error_handlers: List[ErrorHandler] = []
        self._on_argument_type_error_handlers: List[ErrorHandler] = []
        self._on_command_error_handlers: List[CommandErrorHandler] = []
        self._on_command_permission_error_handlers: List[PermissionErrorHandler] = [
        ]
        self.logger: Logger = Logger(log_file)

    # region Декораторы
    def on_before_use_command(self, func: CommandHandler) -> CommandHandler:
        """Декоратор для регистрации обработчиков успешного использования команды."""
        self._on_before_use_command_handlers.append(func)
        return func

    def on_after_use_command(self, func: CommandHandler) -> CommandHandler:
        """Декоратор для регистрации обработчиков успешного использования команды."""
        self._on_after_use_command_handlers.append(func)
        return func

    def on_missing_argument_error(self, func: ErrorHandler) -> ErrorHandler:
        """Декоратор для регистрации обработчиков ошибок аргументов."""
        self._on_missing_argument_error_handlers.append(func)
        return func

    def on_argument_type_error(self, func: ErrorHandler) -> ErrorHandler:
        """Декоратор для регистрации обработчиков ошибок аргументов."""
        self._on_argument_type_error_handlers.append(func)
        return func

    def on_command_error(self, func: CommandErrorHandler) -> CommandErrorHandler:
        """Декоратор для регистрации обработчиков ошибок команд."""
        self._on_command_error_handlers.append(func)
        return func

    def on_command_permission_error(self, func: PermissionErrorHandler) -> PermissionErrorHandler:
        """Декоратор для регистрации обработчиков ошибок команд."""
        self._on_command_permission_error_handlers.append(func)
        return func
    # endregion

    # region Триггеры
    async def _trigger_before_use_command(
        self, message: Message, command: str, args: List[Any], kwargs: Dict[str, Any]
    ) -> None:
        await self.logger._trigger_before_use_command(message, command, args, kwargs)
        for handler in self._on_before_use_command_handlers:
            await handler(message, command, args, kwargs)

    async def _trigger_after_use_command(
        self, message: Message, command: str, args: List[Any], kwargs: Dict[str, Any]
    ) -> None:
        await self.logger._trigger_after_use_command(message, command, args, kwargs)
        for handler in self._on_after_use_command_handlers:
            await handler(message, command, args, kwargs)

    async def _trigger_missing_argument_error(self, message: Message, error: errors.MissingArgumentError) -> None:
        await self.logger._trigger_missing_argument_error(message, error)
        if not self._on_missing_argument_error_handlers:
            raise error
        for handler in self._on_missing_argument_error_handlers:
            await handler(message, error)

    async def _trigger_argument_type_error(self, message: Message, error: errors.ArgumentTypeError) -> None:
        await self.logger._trigger_argument_type_error(message, error)
        if not self._on_argument_type_error_handlers:
            raise error
        for handler in self._on_argument_type_error_handlers:
            await handler(message, error)

    async def _trigger_command_error(self, message: Message, error: errors.CommandError) -> None:
        await self.logger._trigger_command_error(message, error)
        for handler in self._on_command_error_handlers:
            await handler(message, error)

    async def _trigger_command_permission_error(self, message: Message, error: errors.CommandPermissionError) -> None:
        await self.logger._trigger_permissions_error(message, error)
        if not self._on_command_permission_error_handlers:
            raise error
        for handler in self._on_command_permission_error_handlers:
            await handler(message, error)
    # endregion
