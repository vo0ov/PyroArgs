from pyrogram import Client, filters
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("filter_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'hello' with private filter
@PyAr.command(filters=filters.private)
async def hello(message: types.Message, name: str):
    await message.reply(f"Hello, {name}!")

# Run the bot
if __name__ == "__main__":
    app.run()
