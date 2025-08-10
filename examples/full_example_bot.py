from os import environ

from dotenv import load_dotenv
from pyrogram import Client

import pyroargs

# Загрузка переменных окружения
load_dotenv()

#####################
#                   #
#     НАСТРОЙКИ     #
#                   #
#####################

# Инициализация клиента и PyroArgs
app = Client(
    environ['AUTH_NAME'],
    int(environ['AUTH_API_ID']),
    environ['AUTH_API_HASH'],
    bot_token=environ['BOT_TOKEN']
)
PyAr = pyroargs.PyroArgs(app, ('/'))


# Специальная функция для проверки права пользователя
@PyAr.permissions_checker
async def check(
    message: pyroargs.types.Message,
    required_permission: int
) -> bool:
    # * У вас может быть своя функция для проверки прав, это лишь пример * #

    # Списки пользователей с правами
    admninistrators = [123456789]
    moderators = [987654321]

    # Не трогайте, если не знаете как это работает
    user_id = message.from_user.id
    current_permission = 0

    # Проверяем, является ли пользователь модератором
    if user_id in moderators:
        current_permission = 100  # Модератор, уровень прав 100

    # Проверяем, является ли пользователь администратором
    elif user_id in admninistrators:
        current_permission = 999  # Администратор, уровень прав 999

    # Возвращаем True, если у пользователя достаточно прав
    return current_permission >= required_permission

####################
#                  #
#      ИВЕНТЫ      #
#                  #
####################


# Вызывается до выполнения кода в команде
@PyAr.events.on_before_use_command
async def on_before_use_command(
    client: Client,
    command: str,
    args: list,
    kwargs: dict
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    print(f'⏱️ Команда "{command}" начала выполнение...')


# Вызывается после выполнения кода в команде
@PyAr.events.on_after_use_command
async def on_after_use_command(
    client: Client,
    command: str,
    args: list,
    kwargs: dict
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    print(f'✅ Команда "{command}" завершила выполнение!')


# Вызывается при недостаточном количестве аргументов
@PyAr.events.on_missing_argument_error
async def on_missing_argument_error(
    message: pyroargs.types.Message,
    error: pyroargs.errors.missing_argument_error
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    await message.reply(f'❌ Вы пропустили аргумент: `{error.name}`!', quote=True)


# Вызывается при неверном типе аргумента
@PyAr.events.on_argument_type_error
async def on_argument_type_error(
    message: pyroargs.types.Message,
    error: pyroargs.errors.argument_type_error
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    await message.reply(f'❌ Неверный тип аргумента: `{error.name}`!', quote=True)


# Вызывается при возникновении ошибки в команде
@PyAr.events.on_command_error
async def on_command_error(
    message: pyroargs.types.Message,
    error: pyroargs.errors.command_error
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    await message.reply(f'❌ Произошла ошибка в команде: `{error.command}`!', quote=True)


# Вызывается при недостаточном количестве прав у пользователя
@PyAr.events.on_command_permission_error
async def on_command_permission_error(
    message: pyroargs.types.Message,
    error: pyroargs.errors.command_permission_error
) -> None:
    # * У вас может быть своя функция логирования, это лишь пример * #

    await message.reply(f'❌ Недостаточно прав для выполнения команды: `{error.command}`!', quote=True)


###################
#                 #
#     КОМАНДЫ     #
#                 #
###################


# Команда вывода списка всех доступных команд
@PyAr.command(
    description='Выводит список всех доступных команд',
    usage='/help',
    example='/help',
)
async def help(message: pyroargs.types.Message) -> None:
    # Заголовок
    help_text = 'Список доступных команд:\n'

    # Перебираем все категории
    for category, commands in PyAr.registry.iterate_categories_with_commands():
        # Добавляем категорию
        help_text += f'**Категория: {category}**\n'

        # Перебираем все команды
        for cmd in commands:
            # Если у пользователя достаточно прав, то добавляем команду
            if await PyAr.permission_checker_func(message, cmd.permissions):
                # Добавляем команду
                help_text += f'/**{cmd.command}** - `{cmd.description}`\n'
                help_text += f'Использование: `{cmd.usage}`\n'
                help_text += f'Пример: `{cmd.example}`\n\n'

    # Отправляем сообщение
    await message.reply(help_text)


# Команда для повторения текста
@PyAr.command(
    description='Повторяет текст',
    usage='/echo [текст]',
    example='/echo Привет!',
)
async def echo(message: pyroargs.types.Message, *, text: str) -> None:
    # Проверяем текст на пустоту
    if not text:
        # Если текст пустой, то отправляем сообщение об ошибке
        await message.reply('❌ Нельзя отправить пустой текст!', quote=True)
        return

    # Отправляем текст
    await message.reply(text)


@PyAr.command(
    description='Вывод информации о аккаунте',
    usage='/info',
    example='/info',
)
async def info(message: pyroargs.types.Message) -> None:
    # Отправляем информацию о пользователе
    await message.reply(
        f'👤 Имя: `{message.from_user.first_name}`\n'
        f'🆔 ID: `{message.from_user.id}`'
    )


# Команда для фейкового бана
@PyAr.command(
    description='Фейковый бан',
    usage='/ban [пользователь] (время) (причина)',
    example='/ban @user 200 Спам',
    permissions_level=1
)
async def ban(
    message: pyroargs.types.Message,
    user: str,
    ban_time: int = 120,
    *,
    reason: str
) -> None:
    # Фейковый бан
    await message.reply(f'Пользователь `{user}` был забанен на `{ban_time}` секунд по причине: `{reason}`.')


# Команда для вызова ошибки
@PyAr.command(
    description='Вызывает исключение',
    usage='/error',
    example='/error',
)
async def error(message: pyroargs.types.Message) -> None:
    print(1 / 0)  # ВНИМАНИЕ! Это вызовет исключение "ZeroDivisionError" для теста


# Запуск клиента
app.run()
