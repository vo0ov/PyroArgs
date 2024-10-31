from pyrogram import Client, filters
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("private_info_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])

# Определение пользовательского фильтра для приватных чатов
private_filter = filters.private


# Использование custom_data и пользовательского фильтра
@pyro_args.command(custom_filters=private_filter, custom_data="Данные для приватного чата")
async def info(message: types.Message):
    await message.reply(f"Это приватный чат. custom_data: {message.custom_data}")

if __name__ == "__main__":
    bot.run()
