# PyroArgs/types/logger.py
import logging
from typing import List, Dict, Any

from . import Message
from ..errors import ArgumentsError, CommandError, PermissionsError


class Logger:
    def __init__(self) -> None:
        self.use_command = None
        self.arguments_error = None
        self.command_error = None
        self.permissions_error = None

        self.logger = logging.getLogger('PyroArgs')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def __get_username(self, message: Message) -> str:
        if message.from_user.username:
            return f'@{message.from_user.username}'
        return message.from_user.first_name

    # * SETTERS * #
    def set_use_command(
        self,
        message: str = (
            '{user} успешно использовал команду "{command}" с аргументами "{args}" и ключевыми аргументами "{kwargs}".'
        )
    ) -> None:
        self.use_command = message

    def set_arguments_error(
        self,
        message: str = (
            '{user} использовал команду "{command}" с некорректными аргументами "{args}" и ключевыми аргументами "{kwargs}".'
        )
    ) -> None:
        self.arguments_error = message

    def set_command_error(
        self,
        message: str = (
            '{user} использовал команду "{command}" с аргументами "{args}" и '
            'ключевыми аргументами "{kwargs}", но произошла ошибка в коде '
            'команды: "{error}".'
        )
    ) -> None:
        self.command_error = message

    def set_permissions_error(
        self,
        message: str = (
            '{user} использовал команду "{command}" с аргументами "{args}" и '
            'ключевыми аргументами "{kwargs}", но у него недостаточно прав.'
        )
    ) -> None:
        self.permissions_error = message

    # * TRIGGER METHODS * #
    async def trigger_use_command(self, message: Message, command: str, args: List[Any], kwargs: Dict[str, Any]) -> None:
        if self.use_command:
            self.logger.info(self.use_command.format(
                user=self.__get_username(message),
                command=command,
                args=args,
                kwargs=kwargs
            ))

    async def trigger_arguments_error(self, error: ArgumentsError) -> None:
        if self.arguments_error:
            self.logger.info(self.arguments_error.format(
                user=self.__get_username(error.message),
                command=error.command,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs,
                missing_arg=error.missing_arg,
                arg_position=error.arg_position
            ))

    async def trigger_command_error(self, error: CommandError) -> None:
        if self.command_error:
            self.logger.info(self.command_error.format(
                user=self.__get_username(error.message),
                command=error.command,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs,
                error=error.error_message
            ))

    async def trigger_permissions_error(self, error: PermissionsError) -> None:
        if self.permissions_error:
            self.logger.info(self.permissions_error.format(
                user=self.__get_username(error.message),
                command=error.command,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs
            ))
