from pyrogram import Client, filters
from PyroArgs import PyroArgs, types, errors

# Заполните ваши api_id и api_hash
bot = Client("full_featured_bot", api_id=..., api_hash="...")
pyro_args = PyroArgs(bot, prefixes=["/"])

# Список ID администраторов
admins_list = [123456789, 987654321]


# Обработчик ошибок аргументов
@pyro_args.events.on_arguments_error
async def handle_arguments_error(message: types.Message, error: errors.ArgumentsError):
    await message.reply(f"Ошибка аргументов: {error}")


# Обработчик ошибок команд
@pyro_args.events.on_command_error
async def handle_command_error(message: types.Message, error: errors.CommandError):
    await message.reply(f"Ошибка в команде: {error}")


# Команда 'ban' доступна администраторам, и она банит пользователя текущего чата
admin_filter = filters.group & filters.user(admins_list)


@pyro_args.command(custom_filters=admin_filter)
async def ban(message: types.Message, user_id: int):
    try:
        await bot.ban_chat_member(message.chat.id, int(user_id))
        await message.reply(f"Пользователь {user_id} был забанен в этом чате.")
    except Exception as e:
        raise errors.CommandError(f"Не удалось забанить пользователя: {e}")

if __name__ == "__main__":
    bot.run()
