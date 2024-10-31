from pyrogram import Client
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("join_args_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])


# Команда 'join' объединяет произвольное количество аргументов
@pyro_args.command()
async def join(message: types.Message, *, args: str):
    if args:
        combined = args.split()
        await message.reply(f"Объединенные аргументы: {combined}")
    else:
        await message.reply("Пожалуйста, укажите аргументы для объединения.")

if __name__ == "__main__":
    bot.run()
