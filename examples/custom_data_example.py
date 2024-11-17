from pyrogram import Client
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("custom_data_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'version' with custom data
@PyAr.command()
async def version(message: types.Message, version: str = "1.0"):
    await message.reply(f"Version: {version}", quote=True)

# Run the bot
if __name__ == "__main__":
    app.run()
