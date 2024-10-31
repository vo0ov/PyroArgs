from pyrogram import Client
from PyroArgs import PyroArgs, types

# Инициализация клиента Pyrogram
# Заполните ваши api_id и api_hash
bot = Client("greet_bot", api_id=..., api_hash="...")

# Создание экземпляра PyroArgs с префиксом команд
pyro_args = PyroArgs(bot, prefixes=["/"])


# Определение команды 'greet' с одним аргументом 'name'
@pyro_args.command()
async def greet(message: types.Message, name: str):
    await message.reply(f"Привет, {name}!")

# Запуск бота
if __name__ == "__main__":
    bot.run()
