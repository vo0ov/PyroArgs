from pyrogram import Client
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("set_setting_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])

# key и value
key = None


# Команда 'set_setting' с именованным аргументом 'value'
@pyro_args.command()
async def set_setting(message: types.Message, *, value: str):
    global key
    key = value
    await message.reply(f"Установлено: {key} = {value}")

if __name__ == "__main__":
    bot.run()
