from pyrogram import Client
from PyroArgs import PyroArgs, types, errors

# Заполните ваши api_id и api_hash
bot = Client("command_error_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])


# Обработчик ошибок команд
@pyro_args.events.on_command_error
async def handle_command_error(message: types.Message, error: errors.CommandError):
    await message.reply(f"Произошла ошибка при выполнении команды: {error}")


# Команда 'divide' с обработкой исключений
@pyro_args.command()
async def divide(message: types.Message, numerator: int, denominator: int):
    try:
        result = int(numerator) / int(denominator)
        await message.reply(f"Результат деления: {result}")
    except ZeroDivisionError:
        raise errors.CommandError("Деление на ноль невозможно.")
    except ValueError:
        raise errors.CommandError("Пожалуйста, введите два числа.")

if __name__ == "__main__":
    bot.run()
