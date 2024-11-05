![PyPI - Downloads](https://img.shields.io/pypi/dm/PyroArgs?label=%D0%A1%D0%BA%D0%B0%D1%87%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9) ![PyPI - License](https://img.shields.io/pypi/l/PyroArgs?label=%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F)

# [PyroArgs на PyPi](https://pypi.org/project/PyroArgs/)

`PyroArgs` — это библиотека для удобной обработки аргументов команд в [Pyrogram](https://github.com/pyrogram/pyrogram). Она позволяет легко создавать команды с аргументами, обрабатывать ошибки и расширять функциональность с помощью системы событий.

## Особенности

- **Удобный декоратор для создания команд** с поддержкой позиционных и именованных аргументов.
- **Обработка ошибок аргументов и команд** с помощью специальных исключений `ArgumentsError` и `CommandError`.
- **Система событий** для регистрации обработчиков ошибок.
- **Поддержка `custom_data`** для передачи дополнительных данных в команды.
- **Совместимость с пользовательскими фильтрами и группами обработчиков** из Pyrogram.

## Установка

```bash
pip install PyroArgs
```

## Использование

### Импорт необходимых модулей

```python
from pyrogram import Client
from PyroArgs import PyroArgs, types, errors
```

### Инициализация клиента и `PyroArgs`

```python
# Инициализируйте клиент Pyrogram с вашими учетными данными
bot = Client("my_bot", api_id=..., api_hash="...")  # Замените '...' на ваши api_id и api_hash

# Создайте экземпляр PyroArgs с префиксами для команд
pyro_args = PyroArgs(bot, prefixes=["/"])
```

### Создание команды

```python
@pyro_args.command()
async def greet(message: types.Message, name: str):
    await message.reply(f"Привет, {name}!")
```

### Обработка ошибок аргументов

```python
@pyro_args.events.on_arguments_error
async def handle_arguments_error(message: types.Message, error: errors.ArgumentsError):
    await message.reply(f"Ошибка аргументов: {error}")
```

### Обработка ошибок команд

```python
@pyro_args.events.on_command_error
async def handle_command_error(message: types.Message, error: errors.CommandError):
    await message.reply(f"Ошибка в команде: {error}")
```

### Запуск бота

```python
if __name__ == "__main__":
    bot.run()
```

## Полный код из примера выше:

```python
from pyrogram import Client
from PyroArgs import PyroArgs, types, errors

# Заполните ваши api_id и api_hash
bot = Client("my_bot", api_id=..., api_hash="...")  # Замените '...' на ваши api_id и api_hash

# Создание экземпляра PyroArgs с префиксом команд
pyro_args = PyroArgs(bot, prefixes=["/"])

# Создание команды
@pyro_args.command()
async def greet(message: types.Message, name: str):
    await message.reply(f"Привет, {name}!")

# Обработка ошибок аргументов
@pyro_args.events.on_arguments_error
async def handle_arguments_error(message: types.Message, error: errors.ArgumentsError):
    await message.reply(f"Ошибка аргументов: {error}")

# Обработка ошибок команд
@pyro_args.events.on_command_error
async def handle_command_error(message: types.Message, error: errors.CommandError):
    await message.reply(f"Ошибка в команде: {error}")

# Запуск бота
if __name__ == "__main__":
    bot.run()
```

## Примеры

В папке `examples/` представлены различные примеры использования библиотеки PyroArgs:

- [`greet_bot.py`](examples/greet_bot.py): Базовая команда приветствия.
- [`private_info_bot.py`](examples/private_info_bot.py): Использование `custom_data` и пользовательского фильтра.
- [`argument_error_bot.py`](examples/argument_error_bot.py): Обработка ошибки аргументов.
- [`command_error_bot.py`](examples/command_error_bot.py): Обработка исключений внутри команд.
- [`echo_bot.py`](examples/echo_bot.py): Команда с позиционными и именованными аргументами.
- [`admin_only_bot.py`](examples/admin_only_bot.py): Команда доступна только администраторам.
- [`version_bot.py`](examples/version_bot.py): Использование `custom_data` для передачи версии бота.
- [`join_args_bot.py`](examples/join_args_bot.py): Команда с произвольным количеством аргументов.
- [`set_setting_bot.py`](examples/set_setting_bot.py): Команда с именованным аргументом после `*`.
- [`full_featured_bot.py`](examples/full_featured_bot.py): Комплексный бот с полной обработкой ошибок.

## Вклад в проект

Если вы хотите внести свой вклад в развитие `PyroArgs`:

- Создайте форк репозитория.
- Создайте новую ветку для ваших изменений.
- Сделайте коммиты с подробными сообщениями.
- Откройте pull request в основной репозиторий.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [`LICENSE`](LICENSE) или ниже:

```
MIT License
Copyright (c) 2024, vo0ov

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
