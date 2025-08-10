# test_parser.py
import enum
from typing import Optional, Union

import pytest

from pyroargs import errors
from pyroargs.parser import get_command_and_args, parse_command


# ───────────── Тестовые функции ─────────────
def base_func(client: ..., message: ..., user: str, ban_time: int = 120, *, reason: str):
    ...


class Color(enum.Enum):
    RED = 'red'
    BLUE = 'blue'


def f_bool(client: ..., message: ..., flag: bool, *, reason: str = ''):
    ...


def f_union(client: ..., message: ..., v: Union[int, str], *, reason: str = ''):
    ...


def f_optional(client: ..., message: ..., x: Optional[int], *, note: str = ''):
    ...


def f_enum(client: ..., message: ..., color: Color, *, note: str = ''):
    ...


def f_only_pos(client: ..., message: ..., a: int, b: int, *, tail: str = ''):
    ...


def f_need_tail(client: ..., message: ..., a: int, *, tail: str):
    ...


def f_star_args(client: ..., message: ..., *args):
    ...


def f_star_kwargs(client: ..., message: ..., **kwargs):
    ...


# ───────────── parse_command ─────────────

def test_positional_int_and_kwonly():
    args, kwargs = parse_command(base_func, 'Notch 123 "spam links"')
    assert args == ['Notch', 123]
    assert kwargs == {'reason': 'spam links'}


def test_default_used_and_kwonly_takes_one_token():
    # ban_time не парсится из второго токена → используется дефолт 120,
    # KEYWORD_ONLY съедает один токен ("Rule violation" — одна строка в кавычках).
    args, kwargs = parse_command(base_func, 'Notch "Rule violation"')
    assert args == ['Notch', 120]
    assert kwargs == {'reason': 'Rule violation'}


def test_quotes_in_positional_value():
    args, kwargs = parse_command(base_func, '"User Name" 60 "because of spam"')
    assert args == ['User Name', 60]
    assert kwargs == {'reason': 'because of spam'}


def test_missing_required_positional_raises():
    with pytest.raises(errors.MissingArgumentError):
        parse_command(base_func, '')


def test_invalid_int_for_ban_time_results_in_error_or_extra_error():
    # В текущей реализации это закончится ArgumentTypeError (на «лишний» токен),
    # что нам подходит: главное — ошибка.
    with pytest.raises(errors.ArgumentTypeError):
        parse_command(base_func, 'Notch abc "x"')


@pytest.mark.parametrize('raw,expected', [
    ('1', True),
    ('yes', True),
    ('on', True),
    ('0', False),
    ('no', False),
    ('off', False),
])
def test_bool_casts(raw, expected):
    args, kwargs = parse_command(f_bool, f'{raw} "ok"')
    assert args == [expected]
    assert kwargs == {'reason': 'ok'}


def test_union_int_preferred_over_str():
    args, kwargs = parse_command(f_union, '42')
    assert args == [42]
    assert kwargs == {'reason': ''}


def test_optional_empty_string_to_none():
    args, kwargs = parse_command(f_optional, '""')
    assert args == [None]
    assert kwargs == {'note': ''}


def test_enum_value():
    args, kwargs = parse_command(f_enum, 'blue')
    assert args[0] is Color.BLUE
    assert kwargs == {'note': ''}


def test_tail_consumed_into_kwonly_reason():
    args, kwargs = parse_command(base_func, 'Notch 10 "reason" extra')
    assert args == ['Notch', 10]
    assert kwargs == {'reason': 'reason extra'}


def test_required_kwonly_missing_raises():
    with pytest.raises(errors.MissingArgumentError):
        parse_command(f_need_tail, '10')


def test_multiple_positionals_and_tail_token():
    args, kwargs = parse_command(f_only_pos, '1 2 "rest of line here"')
    assert args == [1, 2]
    assert kwargs == {'tail': 'rest of line here'}


def test_star_args_forbidden():
    with pytest.raises(TypeError):
        parse_command(f_star_args, 'whatever')


def test_star_kwargs_forbidden():
    with pytest.raises(TypeError):
        parse_command(f_star_kwargs, 'whatever')


# ───────────── get_command_and_args ─────────────

def test_longest_prefix_wins():
    cmd, rest = get_command_and_args('!!ban Notch 60 "griefing"', ['!', '!!'])
    assert cmd == 'ban'
    assert rest == 'Notch 60 "griefing"'


def test_single_string_prefix():
    cmd, rest = get_command_and_args('!kick Steve', '!')
    assert cmd == 'kick'
    assert rest == 'Steve'


def test_missing_prefix_raises():
    with pytest.raises(Exception):
        get_command_and_args('ban Steve', ['!', '/'])
