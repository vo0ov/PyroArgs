from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple

from pyrogram.filters import Filter as TgFilter


@dataclass
class CommandSpec:
    name: str
    description: str = ''
    aliases: Tuple[str, ...] = ()
    command_filter: Optional[TgFilter] = None


def command(
    name: str,
    *,
        description: str = 'No description provided',
        aliases: Tuple[str, ...] = (),
        command_filter: Optional[TgFilter] = None
) -> Callable[..., Any]:
    def decorator(func) -> Any:
        setattr(func, '__cmd_spec__', CommandSpec(
            name=name,
            description=description,
            aliases=aliases,
            command_filter=command_filter
        ))
        return func

    return decorator
