# PyroArgs/types/logger.py
import logging
from typing import List, Dict, Any

from . import Message
from .. import errors


class Logger:
    def __init__(
        self,
        log_file_name: str = None
    ) -> None:
        self.before_use_command = False
        self.after_use_command = False
        self.missing_argument_error = False
        self.argument_type_error = False
        self.command_error = False
        self.permissions_error = False

        self.before_use_command_message = (
            'User "{user}" wrote command "{command}" with args "{args}" and kwargs "{kwargs}".'
        )
        self.after_use_command_message = (
            'User "{user}" used command "{command}" with args "{args}" and kwargs "{kwargs}".'
        )
        self.missing_argument_error_message = (
            'Error in command "{command}" invoked by user "{user}": '
            'Missing required argument "{missing_arg}" at position {arg_position}. '
            'Parsed arguments: {args}. Parsed keyword arguments: {kwargs}.'
        )

        self.argument_type_error_message = (
            'Error in command "{command}" invoked by user "{user}": '
            'Cannot convert argument "{missing_arg}" to "{required_type}" type at position {arg_position}. '
            'Parsed arguments: {args}. Parsed keyword arguments: {kwargs}.'
        )
        self.command_error_message = (
            'Error in command "{command}" used by "{user}": "{error}".'
        )
        self.permissions_error_message = (
            'Permission error: User "{user}" does not have permission level "{level}" to execute command "{command}".'
        )

        self.logger = logging.getLogger('PyroArgs')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            # Обработчик для вывода в консоль
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # Обработчик для записи в файл (если указано имя файла)
            if log_file_name is not None:
                file_handler = logging.FileHandler(log_file_name)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

    def __get_username(self, message: Message) -> str:
        if message.from_user.username:
            return f'@{message.from_user.username}'
        return message.from_user.first_name

    def setup_logs(self, before_use_command: bool = True, after_use_command: bool = True,
                   missing_argument_error: bool = True, argument_type_error: bool = True,
                   command_error: bool = True, permissions_error: bool = True) -> None:
        self.before_use_command = before_use_command
        self.after_use_command = after_use_command
        self.missing_argument_error = missing_argument_error
        self.argument_type_error = argument_type_error
        self.command_error = command_error
        self.permissions_error = permissions_error

    # * TRIGGER METHODS * #
    async def _trigger_before_use_command(
        self,
        message: Message,
        command: str,
        args: List[Any],
        kwargs: Dict[str, Any]
    ) -> None:
        if self.before_use_command:
            self.logger.info(self.before_use_command_message.format(
                user=self.__get_username(message),
                command=command,
                args=args,
                kwargs=kwargs
            ))

    async def _trigger_after_use_command(
        self, message: Message, command: str, args: List[Any], kwargs: Dict[str, Any]
    ) -> None:
        if self.after_use_command:
            self.logger.info(self.after_use_command_message.format(
                user=self.__get_username(message),
                command=command,
                args=args,
                kwargs=kwargs
            ))

    async def _trigger_missing_argument_error(self, message: Message, error: errors.MissingArgumentError) -> None:
        if self.missing_argument_error:
            self.logger.info(self.missing_argument_error_message.format(
                user=self.__get_username(message),
                command=error.name,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs,
                missing_arg=error.missing_arg_name,
                arg_position=error.missing_arg_position
            ))

    async def _trigger_argument_type_error(self, message: Message, error: errors.ArgumentTypeError) -> None:
        if self.argument_type_error:
            self.logger.info(self.argument_type_error_message.format(
                user=self.__get_username(message),
                command=error.name,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs,
                missing_arg=error.errored_arg_name,
                arg_position=error.errored_arg_position,
                required_type=error.required_type
            ))

    async def _trigger_command_error(self, message: Message, error: errors.CommandError) -> None:
        if self.command_error:
            self.logger.info(self.command_error_message.format(
                user=self.__get_username(message),
                command=error.name,
                args=error.parsed_args,
                kwargs=error.parsed_kwargs,
                error=error.original_error
            ))

    async def _trigger_permissions_error(self, message: Message, error: errors.CommandPermissionError) -> None:
        if self.permissions_error:
            self.logger.info(self.permissions_error_message.format(
                user=self.__get_username(message),
                command=error.name,
                level=error.permission_level
            ))
