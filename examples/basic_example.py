from pyrogram import Client
from PyroArgs import PyroArgs, types


# Initialize client and PyroArgs
app = Client("basic_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'hello' with positional arguments
@PyAr.command()
async def hello(message: types.Message, name: str, age: int):
    await message.reply(f"Hello, {name}! You are {age} years old.")


# Command 'sum' with named arguments
@PyAr.command()
async def sum(message: types.Message, a: int, b: int):
    await message.reply(f"{a} + {b} = {a + b}", quote=True)


# Run the bot
if __name__ == "__main__":
    app.run()
