from pyrogram import Client
from PyroArgs import PyroArgs, types, errors

# Заполните ваши api_id и api_hash
bot = Client("argument_error_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])


# Обработчик ошибки аргументов
@pyro_args.events.on_arguments_error
async def handle_arguments_error(message: types.Message, error: errors.ArgumentsError):
    await message.reply(f"Ошибка аргументов: {error}")


# Команда 'sum' с двумя аргументами
@pyro_args.command()
async def sum(message: types.Message, a: int, b: int):
    try:
        result = int(a) + int(b)
        await message.reply(f"Сумма {a} и {b} равна {result}")
    except ValueError:
        await message.reply("Пожалуйста, введите два числа.")

if __name__ == "__main__":
    bot.run()
