from pyrogram import Client
from PyroArgs import PyroArgs, types, errors


# Initialize client and PyroArgs
app = Client("error_handling", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'divide' with error handling
@PyAr.command()
async def divide(message: types.Message, a: float, b: float):
    try:
        await message.reply(f"{a} / {b} = {a / b}")
    except ZeroDivisionError:
        raise errors.CommandError("Division by zero is not possible!")


# Command error handler
@PyAr.events.on_command_error
async def on_command_error(message: types.Message, error: errors.CommandError):
    text = f'{message.from_user.first_name}, error in command "{error.name}": {error.original_error}! Sorry.'
    await message.reply(text)


# Run the bot
if __name__ == "__main__":
    app.run()
