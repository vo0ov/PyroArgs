# tests/test_commandRegistry.py
import pytest
from PyroArgs.types.command import Command
from PyroArgs.types.commandRegistry import CommandRegistry


@pytest.fixture
def registry():
    return CommandRegistry()


def test_add_and_get_commands(registry):
    cmd1 = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start"
    )
    cmd2 = Command(
        command="stop",
        description="Stops the bot",
        usage="/stop",
        example="/stop"
    )
    registry.add_command(cmd1, "General")
    registry.add_command(cmd2, "Admin")

    general_commands = registry.get_commands_by_category("General")
    admin_commands = registry.get_commands_by_category("Admin")

    assert general_commands == [cmd1]
    assert admin_commands == [cmd2]


def test_find_command(registry):
    cmd1 = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start",
        aliases=["run", "init"]
    )
    registry.add_command(cmd1, "General")

    found_cmd = registry.find_command("start")
    assert found_cmd == cmd1

    found_alias = registry.find_command("run")
    assert found_alias == cmd1

    not_found = registry.find_command("unknown")
    assert not_found is None


def test_iterate_categories(registry):
    cmd1 = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start"
    )
    cmd2 = Command(
        command="stop",
        description="Stops the bot",
        usage="/stop",
        example="/stop"
    )
    registry.add_command(cmd1, "General")
    registry.add_command(cmd2, "Admin")

    categories = list(registry.iterate_categories())
    assert set(categories) == {"General", "Admin"}


def test_iterate_commands(registry):
    cmd1 = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start"
    )
    cmd2 = Command(
        command="stop",
        description="Stops the bot",
        usage="/stop",
        example="/stop"
    )
    registry.add_command(cmd1, "General")
    registry.add_command(cmd2, "Admin")

    commands = list(registry.iterate_commands())
    assert set(commands) == {cmd1, cmd2}


def test_iterate_categories_with_commands(registry):
    cmd1 = Command(
        command="start",
        description="Starts the bot",
        usage="/start",
        example="/start"
    )
    cmd2 = Command(
        command="stop",
        description="Stops the bot",
        usage="/stop",
        example="/stop"
    )
    registry.add_command(cmd1, "General")
    registry.add_command(cmd2, "Admin")

    categories_with_cmds = list(registry.iterate_categories_with_commands())
    expected = [
        ("General", [cmd1]),
        ("Admin", [cmd2])
    ]
    assert categories_with_cmds == expected
