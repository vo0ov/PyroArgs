# tests/test_events.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from PyroArgs.types.events import Events
from PyroArgs.errors.arguments_error import ArgumentsError
from PyroArgs.errors.command_error import CommandError
from PyroArgs.errors.permissions_error import PermissionsError


@pytest.fixture
def events():
    return Events()


@pytest.mark.asyncio
async def test_on_use_command(events):
    handler = AsyncMock()
    events.on_use_command(handler)

    await events._trigger_use_command("Test message", "start", ["arg1"], {"key1": "value1"})
    handler.assert_awaited_once_with("Test message", "start", [
                                     "arg1"], {"key1": "value1"})


@pytest.mark.asyncio
async def test_on_arguments_error(events):
    handler = AsyncMock()
    events.on_arguments_error(handler)

    error = ArgumentsError(
        command="start",
        message="Test message",
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        missing_arg="arg2",
        arg_position=2
    )
    await events._trigger_arguments_error("Test message", error)
    handler.assert_awaited_once_with("Test message", error)


@pytest.mark.asyncio
async def test_on_command_error(events):
    handler = AsyncMock()
    events.on_command_error(handler)

    error = CommandError(
        command="start",
        message="Test message",
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        error_message="An error occurred"
    )
    await events._trigger_command_error("Test message", error)
    handler.assert_awaited_once_with("Test message", error)


@pytest.mark.asyncio
async def test_on_permissions_error(events):
    handler = AsyncMock()
    events.on_permissions_error(handler)

    error = PermissionsError(
        command="start",
        message="Test message",
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"}
    )
    await events._trigger_permissions_error("Test message", error)
    handler.assert_awaited_once_with("Test message", error)
