from pyrogram import Client
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("auto_type_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'example' with auto typed arguments
@PyAr.command()
async def example(message: types.Message, arg1: int, arg2: float):
    # True. (Auto converted str from message text to int)
    print(isinstance(arg1, int))

    # True (Auto converted str from message text to float)
    print(isinstance(arg2, float))

    # Send a reply
    await message.reply(f"arg1: {arg1}, arg2: {arg2}", quote=True)


# Run the bot
if __name__ == "__main__":
    app.run()
