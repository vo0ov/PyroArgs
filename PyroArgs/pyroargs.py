# PyroArgs/pyroargs.py
from .types import Message
from pyrogram import Client
from inspect import signature, Parameter
from pyrogram.handlers import MessageHandler
from .errors import ArgumentsError, CommandError
from pyrogram.filters import Filter, create, command
from typing import Callable, List, Any, Dict, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


class Events:
    def __init__(self) -> None:
        self._on_arguments_error_handlers: List[Callable[[Message], Any]] = []
        self._on_command_error_handlers: List[Callable[[Message], Any]] = []

    def on_arguments_error(self, func: Callable[[Message], Any]) -> Callable[[Message], Any]:
        """Декоратор для регистрации обработчиков ошибок аргументов."""
        self._on_arguments_error_handlers.append(func)
        return func

    def on_command_error(self, func: Callable[[Message], Any]) -> Callable[[Message], Any]:
        """Декоратор для регистрации обработчиков ошибок команд."""
        self._on_command_error_handlers.append(func)
        return func

    async def _trigger_arguments_error(self, message: Message, error: ArgumentsError) -> None:
        """Вызов всех зарегистрированных обработчиков ошибок аргументов."""
        if not self._on_arguments_error_handlers:
            raise error

        for handler in self._on_arguments_error_handlers:
            await handler(message, error)

    async def _trigger_command_error(self, message: Message, error: CommandError) -> None:
        """Вызов всех зарегистрированных обработчиков ошибок команд."""
        if not self._on_command_error_handlers:
            raise error

        for handler in self._on_command_error_handlers:
            await handler(message, error)


class PyroArgs:
    def __init__(self, bot: Client, prefixes: List[str]) -> None:
        self.bot: Client = bot
        self.prefixes: List[str] = prefixes
        self.events: Events = Events()

    async def __run_command(self, func: Callable[..., Any], message: Message) -> Any:
        parts: List[str] = message.text.split()[1:]
        func_signature: List[Parameter] = list(
            signature(func).parameters.values())[1:]

        pos_index: int = 0
        keyword_args: Dict[str, Any] = {}
        positional_args: List[Any] = []

        for param in func_signature:
            if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                if pos_index < len(parts):
                    positional_args.append(parts[pos_index])
                    pos_index += 1
                else:
                    raise ArgumentsError(
                        f'Incorrect arguments in {func.__name__} command.')
            elif param.kind == Parameter.KEYWORD_ONLY:
                if pos_index < len(parts):
                    keyword_args[param.name] = ' '.join(parts[pos_index:])
                    break
                elif param.default is Parameter.empty:
                    raise ArgumentsError(
                        f'Incorrect arguments in {func.__name__} command.')
                else:
                    keyword_args[param.name] = param.default
        try:
            return await func(message, *positional_args, **keyword_args)
        except Exception as error:
            raise CommandError(error)

    def command(
        self,
        custom_filters: Filter = create(lambda *_: True),
        group: int = 0,
        custom_data: Any = None
    ) -> Callable[[F], F]:
        def decorator(func: F) -> F:
            async def handler(client: Client, message: Message) -> None:
                message.custom_data = custom_data
                try:
                    await self.__run_command(func, message)
                except ArgumentsError as error:
                    await self.events._trigger_arguments_error(message, error)
                except CommandError as error:
                    await self.events._trigger_command_error(message, error)

            # Сохраняем handler для доступа в тестах
            func._pyroargs_handler = handler

            self.bot.add_handler(
                MessageHandler(
                    handler,
                    command(func.__name__, self.prefixes) & custom_filters
                ),
                group
            )
            return func
        return decorator
