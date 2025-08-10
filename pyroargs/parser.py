import enum
import inspect
import shlex
from typing import (Any, Callable, Dict, List, Sequence, Tuple, Union,
                    get_args, get_origin)

try:
    import errors
except ImportError:
    from . import errors


def get_command_and_args(text: str, prefixes: Union[Sequence[str], str]) -> Tuple[str, str]:
    text = (text or '').lstrip()

    # Нормализация префиксов
    if isinstance(prefixes, str):
        pref_tuple: Tuple[str, ...] = (prefixes,)
    else:
        pref_tuple = tuple(prefixes)
    if not pref_tuple:
        raise ValueError('Prefixes list is empty.')

    # Самый длинный матч
    prefix = next((p for p in sorted(pref_tuple, key=len, reverse=True) if text.startswith(p)), None)
    if prefix is None:
        raise NameError('Command does not start with prefix.')

    rest = text[len(prefix):].lstrip()
    if not rest:
        raise NameError('Command name is missing.')

    # Команда - первое слово, аргументы - остаток
    if ' ' in rest:
        cmd, args = rest.split(' ', 1)
        args = args.strip()
    else:
        cmd, args = rest, ''

    return cmd, args


def _cast(value: str, annotation: Any) -> Any:
    if annotation in (inspect._empty, Any):
        return value

    origin = get_origin(annotation)
    type_arguments = get_args(annotation)

    # Optional/Union
    if origin is Union:
        last_exc = None
        for type_argument in type_arguments:
            if type_argument is type(None):
                if value == '' or value.lower() in {'none', 'null'}:
                    return None
                continue
            try:
                return _cast(value, type_argument)
            except Exception as e:
                last_exc = e
        raise last_exc or ValueError(f'Cannot cast "{value}" to {annotation}')

    # Enum
    if inspect.isclass(annotation) and issubclass(annotation, enum.Enum):
        for m in annotation:  # by name (case-insensitive) or by value
            if m.name.lower() == value.lower() or str(m.value) == value:
                return m
        raise ValueError(f'Unknown enum value "{value}" for {annotation.__name__}')

    # bool
    if annotation is bool:
        v = value.strip().lower()
        if v in {'1', 'true', 'yes', 'y', 'on', 'да', 'д'}:
            return True
        if v in {'0', 'false', 'no', 'n', 'off', 'нет', 'н'}:
            return False
        raise ValueError(f'Cannot cast "{value}" to bool')

    # Пробуем простой вызов типа
    try:
        return annotation(value)
    except Exception as e:
        raise ValueError(str(e)) from None


def parse_command(func: Callable, args: str) -> Tuple[List[Any], Dict[str, Any]]:
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    # пропускаем служебные client, message
    user_params = params[2:]

    # запрет *args/**kwargs
    for p in user_params:
        if p.kind == p.VAR_POSITIONAL:
            raise TypeError(f'Positional var are not supported. Remove "*{p.name}".')
        if p.kind == p.VAR_KEYWORD:
            raise TypeError(f'Keyword var are not supported. Remove "**{p.name}".')

    tokens: List[str] = shlex.split(args or '', posix=True)
    args_used = 0
    out_args: List[Any] = []
    out_kwargs: Dict[str, Any] = {}

    kw_only_params = [p for p in user_params if p.kind == p.KEYWORD_ONLY]
    if len(kw_only_params) > 1:
        # текущая версия поддерживает только один KEYWORD_ONLY
        raise TypeError('Only one keyword-only parameter is supported.')

    # позиционные (включая POSITIONAL_OR_KEYWORD)
    for p in user_params:
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
            if args_used < len(tokens):
                raw = tokens[args_used]
                try:
                    val = _cast(raw, p.annotation)
                except ValueError:
                    # ПРАВИЛО: мягкий переход к KEYWORD_ONLY только если
                    #  - у позиционного есть дефолт,
                    #  - есть KEYWORD_ONLY,
                    #  - текущий токен — ПОСЛЕДНИЙ (иначе это реальная ошибка ввода).
                    if (
                        p.default is not inspect._empty and kw_only_params and (args_used + 1 == len(tokens))
                    ):
                        out_args.append(p.default)
                        # токен НЕ потребляем — он станет хвостом для KEYWORD_ONLY
                        continue
                    raise errors.ArgumentTypeError(
                        name=p.name, message_object=None,
                        parsed_args=tokens, parsed_kwargs=out_kwargs,
                        errored_arg_name=p.name, errored_arg_position=args_used + 1,
                        required_type=p.annotation
                    ) from None
                else:
                    out_args.append(val)
                    args_used += 1  # потребили токен только при успехе
            else:
                if p.default is inspect._empty:
                    raise errors.MissingArgumentError(
                        name=p.name, message_object=None,
                        missing_arg_name=p.name, missing_arg_position=len(out_args) + 1,
                        parsed_args=tokens, parsed_kwargs=out_kwargs
                    )
                out_args.append(p.default)

    # KEYWORD_ONLY: забирает ВЕСЬ остаток строки (tail)
    if kw_only_params:
        p = kw_only_params[0]
        remainder = ' '.join(tokens[args_used:]).strip()

        if not remainder:
            if p.default is inspect._empty:
                raise errors.MissingArgumentError(
                    name=p.name, message_object=None,
                    missing_arg_name=p.name, missing_arg_position=args_used + 1,
                    parsed_args=tokens, parsed_kwargs=out_kwargs
                )
            out_kwargs[p.name] = p.default
        else:
            try:
                out_kwargs[p.name] = _cast(remainder, p.annotation)
            except ValueError:
                raise errors.ArgumentTypeError(
                    name=p.name, message_object=None,
                    parsed_args=tokens, parsed_kwargs=out_kwargs,
                    errored_arg_name=p.name, errored_arg_position=args_used + 1,
                    required_type=p.annotation
                ) from None

        # мы съели весь хвост
        args_used = len(tokens)

    # лишние токены возможны только если НЕТ KEYWORD_ONLY
    if args_used < len(tokens):
        raise errors.ArgumentTypeError(
            name='__extra__', message_object=None,
            parsed_args=tokens, parsed_kwargs=out_kwargs,
            errored_arg_name='__extra__', errored_arg_position=args_used + 1,
            required_type=None
        )

    return out_args, out_kwargs


if __name__ == '__main__':
    def func(client: ..., message: ..., user: str, ban_time: int = 120, *, reason: str = 'No reason'):
        print('---')
        print(user)
        print('---')
        print(ban_time)
        print('---')
        print(reason)
        print('---')

        print(type(user))
        print(type(ban_time))
        print(type(reason))

    command_text = '''/ban Notch 10 "reason" extra'''

    _, args = get_command_and_args(command_text, '/')
    result_args, result_kwargs = parse_command(func, args.strip())
    print(result_args, result_kwargs)
    # func(..., ..., *result_args, **result_kwargs)
