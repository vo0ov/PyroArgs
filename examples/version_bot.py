from pyrogram import Client
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("version_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])


# Команда 'version' с использованием custom_data
@pyro_args.command(custom_data={"version": "1.0.0"})
async def version(message: types.Message):
    bot_version = message.custom_data.get("version", "неизвестна")
    await message.reply(f"Версия бота: {bot_version}")

if __name__ == "__main__":
    bot.run()
