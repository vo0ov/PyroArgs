# PyroArgs/pyroargs.py
from typing import Callable, List, Any, Dict, TypeVar
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.filters import Filter, create, command
from inspect import signature, Parameter


from .types import Message
from .types.events import Events
from .utils import DataHolder
from .types.command import Command
from .types.commandRegistry import CommandRegistry
from .errors import ArgumentsError, CommandError, PermissionsError

F = TypeVar('F', bound=Callable[..., Any])


class PyroArgs:
    def __init__(self, bot: Client, prefixes: List[str] = ['/']) -> None:
        # Переменные класса
        self.bot: Client = bot
        self.prefixes: List[str] = prefixes
        self.events: Events = Events()
        self.registry: CommandRegistry = CommandRegistry()
        self.permissions_checker_func: Callable[[
            int, Message], bool] = lambda _, __: True
        # Сохраняем объекты для доступа в плагинах
        DataHolder.ClientObj = self.bot
        DataHolder.PyroArgsObj = self
        # Функции для настройки логов
        self.set_use_command: Callable[...,
                                       None] = self.events.logger.set_use_command
        self.set_arguments_error: Callable[...,
                                           None] = self.events.logger.set_arguments_error
        self.set_command_error: Callable[...,
                                         None] = self.events.logger.set_command_error
        self.set_permissions_error: Callable[...,
                                             None] = self.events.logger.set_permissions_error

    async def __run_command(self, func: Callable[..., Any],
                            command_names: str, message: Message,
                            permissions_level: int) -> Any:
        result_name = command_names[0]
        command_prefix = None
        for prefix in self.prefixes:
            for command_name in command_names:
                if message.text.startswith(prefix + command_name):
                    command_prefix = prefix + command_name
                    break

        if not self.permissions_checker_func(permissions_level, message):
            raise PermissionsError(command=result_name,
                                   message=message,
                                   parsed_args=[],
                                   parsed_kwargs={})

        # Извлекаем аргументы после команды, включая новые строки
        args_text = message.text[len(command_prefix):].strip()

        func_signature = list(signature(func).parameters.values())[
            1:]  # Пропускаем 'message'

        pos_index: int = 0
        keyword_args: Dict[str, Any] = {}
        positional_args: List[Any] = []

        # Разделяем аргументы на позиции и ключевые аргументы
        for param in func_signature:
            if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                if pos_index < len(args_text):
                    # Берем первый аргумент до пробела
                    if ' ' in args_text:
                        arg, args_text = args_text.split(' ', 1)
                    else:
                        arg, args_text = args_text, ''
                    positional_args.append(arg)
                    pos_index += 1
                else:
                    # Определяем номер пропущенного аргумента
                    missing_arg = param.name
                    # Позиция аргумента (1-индексация)
                    arg_position = pos_index + 1
                    raise ArgumentsError(
                        command=result_name,
                        message=message,
                        missing_arg=missing_arg,
                        arg_position=arg_position,
                        parsed_args=positional_args,
                        parsed_kwargs=keyword_args
                    )
            elif param.kind == Parameter.KEYWORD_ONLY:
                if args_text:
                    keyword_args[param.name] = args_text
                    break
                elif param.default is not Parameter.empty:
                    keyword_args[param.name] = param.default
                else:
                    missing_arg = param.name
                    arg_position = pos_index + 1
                    raise ArgumentsError(
                        command=result_name,
                        message=message,
                        missing_arg=missing_arg,
                        arg_position=arg_position,
                        parsed_args=positional_args,
                        parsed_kwargs=keyword_args
                    )

        try:
            await func(message, *positional_args, **keyword_args)
            return positional_args, keyword_args
        except Exception as error:
            command_error = CommandError(
                command=result_name,
                message=message,
                parsed_args=positional_args,
                parsed_kwargs=keyword_args,
                error_message=str(error)
            )
            raise command_error

    def command(
        self,
        name: str = None,
        description: str = None,
        usage: str = None,
        example: str = None,
        permissions_level: int = 0,
        aliases: List[str] = None,
        command_meta_data: Any = None,
        category: str = 'General',
        custom_filters: Filter = create(lambda *_: True),
        group: int = 0,
        custom_data: Any = None
    ) -> Callable[[F], F]:
        def decorator(func: F) -> F:
            result_name = name or func.__name__
            all_names = [result_name, *(aliases or [])]

            async def handler(client: Client, message: Message) -> None:
                message.custom_data = custom_data

                try:
                    parsed_args, parsed_kwargs = await self.__run_command(func, all_names, message, permissions_level)
                    await self.events._trigger_use_command(
                        message, result_name, parsed_args, parsed_kwargs)
                except ArgumentsError as error:
                    await self.events._trigger_arguments_error(message, error)
                except CommandError as error:
                    await self.events._trigger_command_error(message, error)
                except PermissionsError as error:
                    await self.events._trigger_permissions_error(message, error)

            # Сохраняем handler для доступа в тестах
            func._pyroargs_handler = handler

            cmd = Command(
                result_name,
                description,
                usage,
                example,
                permissions_level,
                aliases,
                command_meta_data
            )
            self.registry.add_command(cmd, category or 'Other')
            self.bot.add_handler(
                MessageHandler(
                    handler,
                    command(all_names,
                            self.prefixes) & custom_filters
                ),
                group
            )
            return func
        return decorator

    def permissions_checker(self, func: Callable[[int, Message], bool]) -> Callable[[int, Message], bool]:
        self.permissions_checker_func = func
        return func
