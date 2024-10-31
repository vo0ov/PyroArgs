from pyrogram import Client, filters
from PyroArgs import PyroArgs, types

# Заполните ваши api_id и api_hash
bot = Client("admin_only_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])

# Замените на список ID администраторов
admins_list = [123456789, 987654321]

# Фильтр для администраторов
admin_filter = filters.user(admins_list)


# Команда 'shutdown' доступна только администраторам
@pyro_args.command(custom_filters=admin_filter)
async def shutdown(message: types.Message):
    await message.reply("Бот будет выключен.")
    await bot.stop()

if __name__ == "__main__":
    bot.run()
