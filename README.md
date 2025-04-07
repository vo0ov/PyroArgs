<!-- markdownlint-disable-next-line MD041 -->
![PyPI - Downloads](https://img.shields.io/pypi/dm/PyroArgs?label=%D0%A1%D0%BA%D0%B0%D1%87%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9) ![PyPI - License](https://img.shields.io/pypi/l/PyroArgs?label=%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F)

# [PyroArgs на PyPi](https://pypi.org/project/PyroArgs/)

`PyroArgs` — это библиотека для удобной обработки аргументов команд в [Pyrogram](https://github.com/pyrogram/pyrogram). Она позволяет легко создавать команды с аргументами, обрабатывать ошибки и расширять функциональность с помощью системы событий.

## Особенности

- **Удобный декоратор для создания команд** с поддержкой позиционных и именованных аргументов прямо как в библиотеке `Discord.py`
- **Обработка ошибок аргументов и команд** с помощью специальных исключений-ивентов
- **Система событий** для регистрации обработчиков ошибок и событий
- **Поддержка `command_meta_data`** для передачи дополнительных данных в команды
- **Совместимость с пользовательскими фильтрами и группами обработчиков** из Pyrogram

## Установка

- Полная установка `PyroArgs` с использованием `pip` (Лучший вариант):

```bash
pip install PyroArgs[all]
```

- Установка `PyroArgs` с использованием `pip` без `TgCrypto` (Это не безопасно!):

```bash
pip install PyroArgs
```

- Установка `PyroArgs` с использованием через `git` (Для продвинутых пользователей):

```bash
git clone https://github.com/vo0ov/PyroArgs.git
cd PyroArgs
pip install .
```

## Использование библиотеки

### Импорт необходимых модулей

```python
from pyrogram import Client
from PyroArgs import PyroArgs, types, errors
```

### Инициализация клиента и `PyroArgs`

```python
# Замените 12345 и 'abcdef' на ваши api_id и api_hash в этой строке, НО лучше использовать переменные окружения
bot = Client('Bot', api_id=12345, api_hash='abcdef')

# Создание экземпляра PyroArgs с префиксом команд
pyro_args = PyroArgs(bot, prefixes=['/'])
```

### Создание команд

```python
@pyro_args.command()
async def greet(message: types.Message, name: str):
    await message.reply(f'Привет, {name}!')

@pyro_args.command()
async def echo(message: types.Message, *, text: str):
    await message.reply(text if text else '❌ Нельзя отправить пустой текст!')
```

### Запуск бота

```python
if __name__ == '__main__':
    bot.run()
```

## Полный код из примера выше

```python
from pyrogram import Client
from PyroArgs import PyroArgs, types, errors

# Замените 12345 и 'abcdef' на ваши api_id и api_hash в этой строке, НО лучше использовать переменные окружения
bot = Client('Bot', api_id=12345, api_hash='abcdef')

# Создание экземпляра PyroArgs с префиксом команд
pyro_args = PyroArgs(bot, prefixes=['/'])

# Создание просейшей команды
@pyro_args.command()
async def greet(message: types.Message, name: str):
    await message.reply(f'Привет, {name}!')

@pyro_args.command()
async def echo(message: types.Message, *, text: str):
    await message.reply(text if text else '❌ Нельзя отправить пустой текст!')

# Запуск бота
if __name__ == '__main__':
    bot.run()
```

## Пример использования большенства функций `PyroArgs`

В папке [`examples`](examples) присутствуют полный пример использования `PyroArgs`:

- [`full_example_bot.py`](examples/full_example_bot.py) - полный пример использования `PyroArgs`

## Вклад в проект

Если вы хотите внести свой вклад в развитие `PyroArgs`:

- Создайте форк репозитория
- Создайте новую ветку для ваших изменений
- Сделайте коммиты с подробными сообщениями
- Откройте pull request в основной репозиторий

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [`LICENSE`](LICENSE) или ниже:

```License
MIT License
Copyright (c) 2024, vo0ov

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
