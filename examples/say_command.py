from pyrogram import Client
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("auto_type_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'say' with auto typed arguments
@PyAr.command()
async def say(message: types.Message, *, text: str):
    await message.reply(text, quote=True)


# Run the bot
if __name__ == "__main__":
    app.run()
