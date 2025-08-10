import asyncio
import importlib
import inspect
import os
import pkgutil
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Type

from .base import BaseModule


@dataclass
class ModuleRecord:
    """Хранит информацию о загруженном модуле."""

    mod: types.ModuleType
    cls: Type[BaseModule]
    inst: BaseModule
    is_protected: bool


class ModuleLoader:
    """Загружает, выгружает и перезагружает модули."""

    def __init__(self, client, *, base_package: str = 'modules', base_path: str | os.PathLike | None = None) -> None:
        """
        :param base_package: имя пакета, внутри которого искать модули (dotted path).
        :param base_path: необязательный файловый путь; если задан, будет добавлен в sys.path.
        """

        self.client = client
        self.base_package = base_package
        if base_path is not None:
            sys.path.insert(0, str(Path(base_path)))

        self.lock = asyncio.Lock()
        self.loaded: Dict[str, ModuleRecord] = {}

    def _import_and_find(self, dotted: str) -> Tuple[types.ModuleType, Type[BaseModule]]:
        """Импортирует модуль и находит в нём класс-наследник BaseModule."""
        module = importlib.import_module(dotted)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseModule) and obj is not BaseModule:
                return module, obj
        raise RuntimeError(f'В {dotted} нет сабкласса BaseModule')

    def _qualname(self, name: str) -> str:
        """Полное имя модуля с учётом базового пакета."""
        return f'{self.base_package}.{name}'

    # ——— внутренние функции под уже захваченный lock ———
    async def _load_locked(self, name: str, is_protected: bool) -> None:
        if name in self.loaded:
            raise RuntimeError(f'Модуль {name} уже загружен')

        dotted = self._qualname(name)
        if dotted in sys.modules:
            del sys.modules[dotted]

        mod, cls = self._import_and_find(dotted)
        inst: BaseModule = cls(self, self.client)
        await inst._load()

        self.loaded[name] = ModuleRecord(mod, cls, inst, is_protected)

    async def _unload_locked(self, name: str) -> None:
        rec = self.loaded.get(name)
        if not rec:
            raise RuntimeError(f'{name} не загружен')

        if rec.is_protected:
            raise RuntimeError(f'Модуль {name} защищён от выгрузки и перезагрузки')

        await rec.inst._unload()
        self.loaded.pop(name)

        dotted = self._qualname(name)
        if dotted in sys.modules:
            del sys.modules[dotted]

    # ——— публичный API для всех (берут lock один раз) ———
    async def load(self, name: str, is_protected: bool = False) -> None:
        """Загружает модуль по имени, если он еще не загружен."""

        async with self.lock:
            await self._load_locked(name, is_protected)

    async def unload(self, name: str) -> None:
        """Выгружает модуль по имени, если он загружен."""

        async with self.lock:
            await self._unload_locked(name)

    async def reload(self, name: str, is_protected: bool = False) -> None:
        """Перезагружает модуль по имени."""

        async with self.lock:
            if name not in self.loaded:
                await self._load_locked(name, is_protected)
                return

            prev_is_protected = self.loaded[name].is_protected

            await self._unload_locked(name)
            await self._load_locked(name, is_protected or prev_is_protected)

    def list_available(self) -> list[str]:
        """Вернёт список доступных модулей внутри base_package (без загруженности)."""

        pkg = importlib.import_module(self.base_package)
        names = []
        for mod in pkgutil.iter_modules(getattr(pkg, '__path__', [])):
            if not mod.ispkg:
                names.append(mod.name)
        return sorted(names)
