from pyrogram import Client
from PyroArgs import PyroArgs, types

# Initialize client and PyroArgs
app = Client("permissions_example", api_id=12345, api_hash="abcdef")
PyAr = PyroArgs(app, ['/', '!'])


# Permissions checker function
@PyAr.permissions_checker
async def check(message: types.Message, required_permission: int):
    current_permission = 0

    if message.from_user.id in [123456789, 987654321]:  # Admins users ids list
        current_permission = 999

    return current_permission >= required_permission


# Command 'admin' with permissions
@PyAr.command(permissions_level=999)
async def admin(message: types.Message):
    await message.reply("You are an admin!")


# Command 'user' with permissions
@PyAr.command()  # default permissions_level is 0
async def user(message: types.Message):
    await message.reply("You are a user!")

# Run the bot
if __name__ == "__main__":
    app.run()
