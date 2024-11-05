# tests/test_command.py
from PyroArgs.types.command import Command


def test_command_creation():
    cmd = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start",
        permissions=1,
        command_meta_data={"key": "value"},
        aliases=["run", "init"]
    )
    assert cmd.command == "start"
    assert cmd.description == "Starts the bot"
    assert cmd.usage == "/start"
    assert cmd.example == "/start"
    assert cmd.permissions == 1
    assert cmd.command_meta_data == {"key": "value"}
    assert cmd.aliases == ["run", "init"]


def test_has_permission():
    cmd = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start",
        permissions=2
    )
    assert cmd.has_permission(3) == True
    assert cmd.has_permission(2) == True
    assert cmd.has_permission(1) == False
