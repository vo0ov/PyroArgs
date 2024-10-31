from pyrogram import Client
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("echo_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])


# Команда 'echo' с позиционными и именованными аргументами
@pyro_args.command()
async def echo(message: types.Message, text: str, *, times: int = 1):
    for _ in range(int(times)):
        await message.reply(text)

if __name__ == "__main__":
    bot.run()
