# PyroArgs/types/events.py
from typing import Any, Callable, Dict, List, TypeAlias

from pyrogram.types import Message

from .. import errors

CommandHandler: TypeAlias = Callable[[
    str, str, List[Any], Dict[str, Any]], Any]

ErrorHandler: TypeAlias = Callable[[Message, errors.ArgumentsError], Any]

CommandErrorHandler: TypeAlias = Callable[[Message, errors.CommandError], Any]

PermissionErrorHandler: TypeAlias = Callable[[
    Message, errors.CommandPermissionError], Any]


class Events:
    def __init__(self) -> None:
        self._on_before_use_command_handlers: List[CommandHandler] = []
        self._on_after_use_command_handlers: List[CommandHandler] = []
        self._on_missing_argument_error_handlers: List[ErrorHandler] = []
        self._on_argument_type_error_handlers: List[ErrorHandler] = []
        self._on_command_error_handlers: List[CommandErrorHandler] = []
        self._on_command_permission_error_handlers: List[PermissionErrorHandler] = []

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

    def on_command_error(
            self,
            func: CommandErrorHandler
    ) -> CommandErrorHandler:
        """Декоратор для регистрации обработчиков ошибок команд."""

        self._on_command_error_handlers.append(func)
        return func

    def on_command_permission_error(
            self,
            func: PermissionErrorHandler
    ) -> PermissionErrorHandler:
        """Декоратор для регистрации обработчиков ошибок команд."""

        self._on_command_permission_error_handlers.append(func)
        return func
    # endregion

    # region Триггеры
    async def _trigger_before_use_command(
        self,
        message: Message,
        command: str,
        args: List[Any],
        kwargs: Dict[str, Any]
    ) -> None:
        for handler in self._on_before_use_command_handlers:
            await handler(message, command, args, kwargs)

    async def _trigger_after_use_command(
        self,
        message: Message,
        command: str,
        args: List[Any],
        kwargs: Dict[str, Any]
    ) -> None:
        for handler in self._on_after_use_command_handlers:
            await handler(message, command, args, kwargs)

    async def _trigger_missing_argument_error(
            self,
            message: Message,
            error: errors.missing_argument_error
    ) -> None:
        if not self._on_missing_argument_error_handlers:
            raise error
        for handler in self._on_missing_argument_error_handlers:
            await handler(message, error)

    async def _trigger_argument_type_error(
            self,
            message: Message,
            error: errors.argument_type_error
    ) -> None:
        if not self._on_argument_type_error_handlers:
            raise error
        for handler in self._on_argument_type_error_handlers:
            await handler(message, error)

    async def _trigger_command_error(
            self,
            message: Message,
            error: errors.command_error
    ) -> None:
        for handler in self._on_command_error_handlers:
            await handler(message, error)

    async def _trigger_command_permission_error(
            self,
            message: Message,
            error: errors.command_permission_error
    ) -> None:
        if not self._on_command_permission_error_handlers:
            raise error
        for handler in self._on_command_permission_error_handlers:
            await handler(message, error)
    # endregion
