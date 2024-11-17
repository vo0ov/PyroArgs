from pyrogram import Client
from PyroArgs import PyroArgs, types, errors

# Initialize client and PyroArgs
app = Client("auto_type_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# This event is called before the command is used
@PyAr.events.on_before_use_command
async def on_before_use_command(message: types.Message, command: str, args: list, kwargs: dict):
    await message.reply(f'Before command {command} used!', quote=True)


# This event is called after the command is used
@PyAr.events.on_after_use_command
async def on_after_use_command(message: types.Message, command: str, args: list, kwargs: dict):
    await message.reply(f'Command {command} used!', quote=True)


# This event is called when a missing argument error occurs
@PyAr.events.on_missing_argument_error
async def on_missing_argument_error(message: types.Message, error: errors.MissingArgumentError):
    await message.reply(f'Missing argument error! Error: {error}', quote=True)


# This event is called when an argument type error occurs
@PyAr.events.on_argument_type_error
async def on_argument_type_error(message: types.Message, error: errors.ArgumentTypeError):
    await message.reply(f'Argument type error! Error: {error}', quote=True)


# This event is called when a command error occurs
@PyAr.events.on_command_error
async def on_command_error(message: types.Message, error: errors.CommandError):
    await message.reply('Command error!', quote=True)


# This event is called when a command permission error occurs
@PyAr.events.on_command_permission_error
async def on_command_permission_error(message: types.Message, error: errors.CommandPermissionError):
    await message.reply('Command permission error!', quote=True)


# Raise a command error
@PyAr.command()
async def raise_error(message: types.Message):
    1/0  # This will raise a ZeroDivisionError


# Run the bot
if __name__ == "__main__":
    app.run()
