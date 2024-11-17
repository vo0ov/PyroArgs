from pyrogram import Client, filters
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("auto_type_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Command 'example' with auto typed arguments
@PyAr.command('example',  # Add command name
              description='Example command',  # Add command description
              usage='example <arg1> <arg2>',  # Add command usage
              example='example 1 2.0',  # Add command example usage
              permissions_level=999,  # Check in PyAr.permissions_checker decorator
              aliases=['ex'],  # Add command aliases
              category='General',  # Add command category
              command_meta_data={'key': 'value'},  # Add command meta data
              filters=filters.private,  # Add private filter
              group=0  # Add group
              )
async def example(message: types.Message, arg1: int, arg2: float):
    # True. (Auto converted str from message text to int)
    print(isinstance(arg1, int))

    # True (Auto converted str from message text to float)
    print(isinstance(arg2, float))

    # Get command_meta_data
    print(message.command_meta_data)

    # Send a reply
    await message.reply(f"arg1: {arg1}, arg2: {arg2}, command_meta_data: {message.command_meta_data}", quote=True)


# Run the bot
if __name__ == "__main__":
    app.run()
