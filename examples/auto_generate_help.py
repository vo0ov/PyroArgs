from pyrogram import Client
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("auto_type_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'help' with auto generated help
@PyAr.command('help', 'Список команд', category='🔧 Основные')
async def help(message: types.Message):
    text = '**📚 Список команд:\n**'
    for category, cmds in PyAr.registry.iterate_categories_with_commands():
        text += f'\n**{category}**:\n'
        for cmd in cmds:
            text += f'•  `v?{cmd.command}` - {cmd.description}\n'

    await message.reply(text, quote=True)


# Run the bot
if __name__ == "__main__":
    app.run()
