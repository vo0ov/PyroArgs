from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List

from pyrogram import Client, filters
from pyrogram.handlers import (CallbackQueryHandler, MessageHandler,
                               RawUpdateHandler)
from pyrogram.handlers.handler import Handler

from .commands import CommandSpec

if TYPE_CHECKING:
    from core.loader import ModuleLoader


@dataclass
class HandlerRef:
    """Ссылка на обработчик, который хранит сам обработчик и группу.

    Это нужно для того, чтобы потом можно было легко удалить обработчик.
    """

    handler: Handler
    group: int = 0


class BaseModule:
    """
    Базовый класс для всех модулей.

    Модули должны наследоваться от этого класса и реализовывать методы on_load и on_unload.
    Также вместо on_load и on_unload можно просто использовать декоратор @command для регистрации команд.
    """

    # Метаданные модуля
    name: str = 'Unnamed'
    description: str = 'No description provided'
    version: str = '1.0'
    auto_bind_commands: bool = True

    # Переменные, которые будут заполнены при инициализации
    loader: ModuleLoader
    client: Client
    _handlers: List[HandlerRef]

    # Автоматическая привязка команд (не трогать, так как этим управляет сам класс)
    __cmd_specs__: tuple[tuple[str, CommandSpec]]

    def __init__(self, loader: ModuleLoader, client: Client) -> None:
        """Инициализация базового модуля."""

        # Сохраняем клиент и контекст
        self.loader = loader
        self.client = client
        self._handlers: List[HandlerRef] = []

        # Если нужно, автоматически связываем команды
        if self.auto_bind_commands:
            for method_name, spec in self.__class__.__cmd_specs__:
                method = getattr(self, method_name)
                command_filter = filters.command([spec.name, *spec.aliases])

                if spec.command_filter:
                    command_filter = command_filter & spec.command_filter

                self.add(MessageHandler(method, command_filter))

    def __init_subclass__(cls, **kwargs) -> None:
        """Автоматически собираем команды при создании подкласса."""

        super().__init_subclass__(**kwargs)

        specs: list[tuple[str, CommandSpec]] = []
        for name, obj in cls.__dict__.items():
            spec: CommandSpec | None = getattr(obj, '__cmd_spec__', None)
            if spec:
                specs.append((name, spec))

        cls.__cmd_specs__ = tuple(specs)

    # ——— Внутренний API ТОЛЬКО для ModuleLoader ———
    async def _load(self) -> None:
        """Загружает модуль, вызывая on_load."""

        await self.on_load()

    async def _unload(self) -> None:
        """Выгружает модуль, вызывая on_unload и снимая все хендлеры."""

        for r in self._handlers:
            self.client.remove_handler(r.handler, group=r.group)

        self._handlers.clear()
        await self.on_unload()

    # ——— Жизненный цикл модуля ———
    async def on_load(self) -> None:
        """Вызывается при загрузке модуля. Здесь можно инициализировать ресурсы, подписаться на события и т.д."""

        ...

    async def on_unload(self) -> None:
        """Вызывается при выгрузке модуля. Здесь можно освободить ресурсы, отписаться от событий и т.д."""

        ...

    # ——— Вспомогательные функции для добавления событий, но так как есть дерокатор они не нужны ———
    def add(self, h: Handler, group: int = 0) -> None:
        """Добавляет обработчик в клиент Pyrogram и сохраняет его для последующего удаления."""

        self.client.add_handler(h, group=group)
        self._handlers.append(HandlerRef(h, group))

    def add_message(self, callback, flt, group: int = 0) -> None:
        """Добавляет обработчик для текстовых сообщений."""

        self.add(MessageHandler(callback, flt), group)

    def add_callback(self, callback, flt, group: int = 0) -> None:
        """Добавляет обработчик для callback_query."""

        self.add(CallbackQueryHandler(callback, flt), group)

    def add_raw(self, callback, group: int = 0) -> None:
        """Добавляет обработчик для "сырых" обновлений."""

        self.add(RawUpdateHandler(callback), group)

    @classmethod
    def iter_commands(cls) -> Iterable[tuple[str, CommandSpec]]:
        """Публичный способ получить пары (method_name, CommandSpec)."""

        return tuple(cls.__cmd_specs__)
