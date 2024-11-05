# tests/test_pyroargs.py
import pytest
from PyroArgs.pyroargs import PyroArgs
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def pyroargs(mock_client):
    return PyroArgs(bot=mock_client)


@pytest.mark.asyncio
async def test_register_command(pyroargs):
    @pyroargs.command(
        name="test",
        description="Test command",
        usage="/test <arg>",
        example="/test value",
        permissions_level=1,
        aliases=["t"]
    )
    async def _(message, arg):
        pass

    command = pyroargs.registry.get_commands_by_category("General")[0]
    assert command.command == "test"
    assert "t" in command.aliases


@pytest.mark.asyncio
async def test_run_command_success(pyroargs):
    @pyroargs.command(
        name="echo",
        description="Echoes the argument",
        usage="/echo <text>",
        example="/echo hello"
    )
    async def echo_command(message, text):
        # Simulate command action
        return text

    handler = echo_command._pyroargs_handler
    mock_message = MagicMock()
    mock_message.text = "/echo hello"

    # Мокируем функцию обработчика события использования команды
    pyroargs.events._trigger_use_command = AsyncMock()

    await handler(pyroargs.bot, mock_message)

    pyroargs.events._trigger_use_command.assert_awaited_once_with(
        mock_message,
        "echo",
        ["hello"],
        {}
    )


@pytest.mark.asyncio
async def test_run_command_arguments_error(pyroargs):
    @pyroargs.command(
        name="echo",
        description="Echoes the argument",
        usage="/echo <text>",
        example="/echo hello"
    )
    async def echo_command(message, text):
        return text

    handler = echo_command._pyroargs_handler
    mock_message = MagicMock()
    mock_message.text = "/echo"  # Отсутствует необходимый аргумент

    # Мокируем функции обработчика событий
    pyroargs.events._trigger_arguments_error = AsyncMock()
    pyroargs.events._trigger_use_command = AsyncMock()
    pyroargs.events._trigger_command_error = AsyncMock()
    pyroargs.events._trigger_permissions_error = AsyncMock()

    await handler(pyroargs.bot, mock_message)

    pyroargs.events._trigger_arguments_error.assert_awaited_once()
    pyroargs.events._trigger_use_command.assert_not_called()
    pyroargs.events._trigger_command_error.assert_not_called()
    pyroargs.events._trigger_permissions_error.assert_not_called()


@pytest.mark.asyncio
async def test_run_command_command_error(pyroargs):
    @pyroargs.command(
        name="fail",
        description="Command that fails",
        usage="/fail",
        example="/fail"
    )
    async def fail_command(message):
        raise ValueError("Intentional Error")

    handler = fail_command._pyroargs_handler
    mock_message = MagicMock()
    mock_message.text = "/fail"

    # Мокируем функции обработчика событий
    pyroargs.events._trigger_command_error = AsyncMock()

    await handler(pyroargs.bot, mock_message)

    pyroargs.events._trigger_command_error.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_command_permissions_error(pyroargs):
    @pyroargs.command(
        name="admin",
        description="Admin command",
        usage="/admin",
        example="/admin",
        permissions_level=2
    )
    async def admin_command(message):
        pass

    handler = admin_command._pyroargs_handler
    mock_message = MagicMock()
    mock_message.text = "/admin"

    # Устанавливаем функцию проверки прав, которая возвращает False
    pyroargs.permissions_checker(lambda level, msg: False)

    # Мокируем функции обработчика событий
    pyroargs.events._trigger_permissions_error = AsyncMock()

    await handler(pyroargs.bot, mock_message)

    pyroargs.events._trigger_permissions_error.assert_awaited_once()


@pytest.mark.asyncio
async def test_permissions_checker(pyroargs):
    def check_permissions(level, message):
        return level >= 1

    pyroargs.permissions_checker(check_permissions)
    assert pyroargs.permissions_checker_func == check_permissions
